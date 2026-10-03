"""Tests for src/agents/agent.py. The LLM, the MCP client and the compiled
LangGraph agent are all replaced with small fakes, so these run with no API
key, no subprocess and no network.
"""

import asyncio
from datetime import date
from types import SimpleNamespace

import pytest
from langchain_core.messages import HumanMessage
from langgraph.errors import GraphRecursionError

from src.agents import agent
from src.config import constants
from src.exceptions import (
    AgentError,
    AgentLoopError,
    AgentTimeoutError,
    DataNotFoundError,
    InvalidInputError,
    LLMRateLimitError,
    LLMServiceError,
)


@pytest.fixture(autouse=True)
def clean_agent_state(monkeypatch):
    """agent.py keeps its state at module level, so every test starts from
    (and restores) an empty state, and never really sleeps or logs to disk."""
    saved_state = dict(agent._state)
    saved_order = list(agent._session_order)
    agent._state.update(agent=None, stack=None, system_prompt=None)
    agent._session_order.clear()

    async def no_sleep(_seconds):
        return None

    monkeypatch.setattr(agent.asyncio, "sleep", no_sleep)
    yield
    agent._state.clear()
    agent._state.update(saved_state)
    agent._session_order[:] = saved_order


def ai_message(content="", tool_calls=None, usage=None):
    """Stand-in for an AIMessage: ask() only reads these three attributes."""
    return SimpleNamespace(content=content, tool_calls=tool_calls or [], usage_metadata=usage)


class FakeAgent:
    """Returns / raises the queued outcomes, one per ainvoke() call."""

    def __init__(self, *outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0
        self.last_config = None

    async def ainvoke(self, payload, config=None):
        self.calls += 1
        self.last_config = config
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


def simple_result(text="the answer"):
    return {"messages": [HumanMessage(content="q"), ai_message(text)]}


@pytest.fixture
def captured_logs(monkeypatch):
    calls = []
    monkeypatch.setattr(agent, "log_call", lambda **kwargs: calls.append(kwargs))
    return calls


def run(coroutine):
    return asyncio.run(coroutine)


class TestBuildSystemPrompt:
    def test_anchors_today_to_the_dataset_date(self, monkeypatch):
        monkeypatch.setattr(agent, "get_dataset_today", lambda: date(2013, 1, 2))
        assert "2013-01-02" in agent.build_system_prompt()

    def test_falls_back_to_the_real_date_when_dataset_is_unreadable(self, monkeypatch):
        def broken():
            raise DataNotFoundError("no data yet")

        monkeypatch.setattr(agent, "get_dataset_today", broken)
        assert date.today().isoformat() in agent.build_system_prompt()


class TestErrorClassification:
    def test_known_connection_error_names_are_detected(self):
        error = type(constants.CONNECTION_ERROR_NAMES[0], (Exception,), {})()
        assert agent._is_connection_error(error) is True

    def test_other_errors_are_not_connection_errors(self):
        assert agent._is_connection_error(ValueError("x")) is False

    def test_rate_limit_detected_by_status_code(self):
        error = Exception("boom")
        error.status_code = 429
        assert agent._is_rate_limit_error(error) is True

    def test_rate_limit_detected_by_message(self):
        assert agent._is_rate_limit_error(Exception("rate_limit_exceeded for org")) is True
        assert agent._is_rate_limit_error(Exception("Limit 6000 tokens per minute")) is True

    def test_rate_limit_found_in_the_exception_chain(self):
        inner = Exception("x")
        inner.status_code = 413
        outer = RuntimeError("wrapped")
        outer.__cause__ = inner
        assert agent._is_rate_limit_error(outer) is True

    def test_plain_error_is_not_a_rate_limit(self):
        assert agent._is_rate_limit_error(RuntimeError("something else")) is False

    def test_circular_exception_chain_does_not_loop_forever(self):
        first, second = RuntimeError("a"), RuntimeError("b")
        first.__cause__ = second
        second.__cause__ = first
        assert agent._is_rate_limit_error(first) is False


class TestTrimming:
    def test_short_history_is_returned_untouched(self, monkeypatch):
        monkeypatch.setattr(constants, "AGENT_HISTORY_TURNS", 3)
        messages = [HumanMessage(content="a"), ai_message("b")]
        assert agent._trim_for_model(messages) is messages

    def test_keeps_only_the_most_recent_human_turns(self, monkeypatch):
        monkeypatch.setattr(constants, "AGENT_HISTORY_TURNS", 1)
        first, reply1 = HumanMessage(content="one"), ai_message("r1")
        second, reply2 = HumanMessage(content="two"), ai_message("r2")
        assert agent._trim_for_model([first, reply1, second, reply2]) == [second, reply2]

    def test_trimming_starts_at_a_human_message_boundary(self, monkeypatch):
        monkeypatch.setattr(constants, "AGENT_HISTORY_TURNS", 2)
        h1, h2, h3 = (HumanMessage(content=str(n)) for n in (1, 2, 3))
        tool_turn = ai_message("", tool_calls=[{"name": "t", "args": {}, "id": "1"}])
        trimmed = agent._trim_for_model([h1, tool_turn, h2, tool_turn, h3])
        assert trimmed[0] is h2

    def test_pre_model_hook_wraps_the_trimmed_messages(self, monkeypatch):
        monkeypatch.setattr(constants, "AGENT_HISTORY_TURNS", 1)
        h1, h2 = HumanMessage(content="1"), HumanMessage(content="2")
        assert agent._pre_model_hook({"messages": [h1, h2]}) == {"llm_input_messages": [h2]}


class TestExtractText:
    def test_plain_string(self):
        assert agent._extract_text("hello") == "hello"

    def test_list_of_blocks_keeps_only_text(self):
        content = ["a", {"type": "text", "text": "b"}, {"type": "image", "url": "x"}, 5]
        assert agent._extract_text(content) == "ab"

    def test_anything_else_is_stringified(self):
        assert agent._extract_text(42) == "42"


class TestClearSession:
    def test_forgets_the_session_and_deletes_its_memory(self):
        deleted = []
        agent._state["checkpointer"] = SimpleNamespace(delete_thread=deleted.append)
        agent._session_order.extend(["a", "b"])
        agent.clear_session("a")
        assert agent._session_order == ["b"]
        assert deleted == ["a"]

    def test_is_safe_when_the_agent_is_not_running_or_session_unknown(self):
        agent._state["checkpointer"] = None
        agent.clear_session("never-seen")   # must not raise


class TestTrackSession:
    def test_oldest_session_ages_out_past_the_cap(self, monkeypatch):
        monkeypatch.setattr(constants, "CHAT_MAX_SESSIONS", 2)
        for name in ("a", "b", "c"):
            agent._track_session(name)
        assert agent._session_order == ["b", "c"]

    def test_reusing_a_session_moves_it_to_the_end(self, monkeypatch):
        monkeypatch.setattr(constants, "CHAT_MAX_SESSIONS", 5)
        for name in ("a", "b", "a"):
            agent._track_session(name)
        assert agent._session_order == ["b", "a"]


class TestInitAndShutdown:
    def test_init_builds_once_and_reuses_the_agent(self, monkeypatch):
        builds = []

        async def fake_build():
            builds.append(1)
            return "the-agent", "the-stack", "the-prompt", 4, "the-memory"

        monkeypatch.setattr(agent, "_build_agent", fake_build)
        assert run(agent.init_agent()) == "the-agent"
        assert run(agent.init_agent()) == "the-agent"
        assert len(builds) == 1
        assert agent._state["stack"] == "the-stack"
        assert agent._state["checkpointer"] == "the-memory"
        assert agent._state["system_prompt"] == "the-prompt"

    def test_init_failure_becomes_agent_error(self, monkeypatch):
        async def failing_build():
            raise RuntimeError("cannot start subprocess")

        monkeypatch.setattr(agent, "_build_agent", failing_build)
        with pytest.raises(AgentError):
            run(agent.init_agent())
        assert agent._state["agent"] is None

    def test_shutdown_without_a_stack_is_a_noop(self):
        run(agent.shutdown_agent())  # should not raise

    def test_shutdown_closes_the_stack_and_clears_state(self):
        closed = []

        class Stack:
            async def aclose(self):
                closed.append(True)

        agent._state.update(agent="a", stack=Stack())
        run(agent.shutdown_agent())
        assert closed == [True]
        assert agent._state["agent"] is None and agent._state["stack"] is None

    def test_shutdown_survives_a_slow_stack(self, monkeypatch):
        monkeypatch.setattr(constants, "AGENT_STOP_TIMEOUT_SECONDS", 0.01)

        class SlowStack:
            async def aclose(self):
                await asyncio.Event().wait()  # never finishes

        agent._state.update(agent="a", stack=SlowStack())
        run(agent.shutdown_agent())  # logs a warning, does not raise

    def test_shutdown_survives_a_failing_stack(self):
        class BrokenStack:
            async def aclose(self):
                raise RuntimeError("already dead")

        agent._state.update(agent="a", stack=BrokenStack())
        run(agent.shutdown_agent())  # logs, does not raise

    def test_restart_closes_the_old_stack_and_rebuilds(self, monkeypatch):
        closed = []

        class OldStack:
            async def aclose(self):
                closed.append(True)
                raise RuntimeError("connection already broken")  # must be swallowed

        async def fake_init():
            return "fresh-agent"

        monkeypatch.setattr(agent, "init_agent", fake_init)
        agent._state.update(agent="old", stack=OldStack())
        assert run(agent._restart_agent()) == "fresh-agent"
        assert closed == [True]
        assert agent._state["agent"] is None  # init_agent (faked) is what repopulates it


class TestBuildAgent:
    def test_wires_client_tools_model_and_prompt_together(self, monkeypatch):
        seen = {}

        class FakeSession:
            async def __aenter__(self):
                return "mcp-session"

            async def __aexit__(self, *exc_info):
                return False

        class FakeClient:
            def __init__(self, servers):
                seen["servers"] = servers

            def session(self, name):
                seen["session_name"] = name
                return FakeSession()

        async def fake_load_tools(session):
            seen["tools_session"] = session
            return ["tool-1", "tool-2"]

        class FakeLLM:
            def __init__(self, **kwargs):
                seen["llm_kwargs"] = kwargs

            def bind_tools(self, tools, parallel_tool_calls):
                seen["bound"] = (tools, parallel_tool_calls)
                return "llm-with-tools"

        def fake_create_agent(llm, tools, prompt=None, checkpointer=None, pre_model_hook=None):
            seen["create"] = (llm, tools, prompt, checkpointer, pre_model_hook)
            return "compiled-agent"

        monkeypatch.setattr(agent, "MultiServerMCPClient", FakeClient)
        monkeypatch.setattr(agent, "load_mcp_tools", fake_load_tools)
        monkeypatch.setattr(agent, "ChatGroq", FakeLLM)
        monkeypatch.setattr(agent, "create_react_agent", fake_create_agent)
        monkeypatch.setattr(agent, "MemorySaver", lambda: "memory")
        monkeypatch.setattr(agent, "build_system_prompt", lambda: "BASE PROMPT")

        async def build_and_close():
            result = await agent._build_agent()
            await result[1].aclose()
            return result

        built_agent, _stack, prompt, tool_count, checkpointer = run(build_and_close())

        assert built_agent == "compiled-agent"
        assert checkpointer == "memory"   # kept so clear_session() can wipe a thread
        assert tool_count == 2
        assert prompt.startswith("BASE PROMPT") and "CRITICAL SYSTEM RULES" in prompt
        assert seen["session_name"] == constants.MCP_SERVER_NAME
        assert seen["tools_session"] == "mcp-session"
        assert seen["bound"] == (["tool-1", "tool-2"], False)
        assert seen["llm_kwargs"]["model"] == constants.AGENT_MODEL_NAME
        assert seen["create"][0] == "llm-with-tools"
        assert seen["create"][3] == "memory"
        assert seen["create"][4] is agent._pre_model_hook
        server = seen["servers"][constants.MCP_SERVER_NAME]
        assert server["args"] == ["-m", constants.MCP_SERVER_MODULE]
        assert server["transport"] == constants.MCP_TRANSPORT


class TestAsk:
    def test_refuses_when_the_agent_is_not_running(self):
        with pytest.raises(AgentError):
            run(agent.ask("hello"))

    def test_returns_the_final_text_and_logs_the_call(self, captured_logs):
        fake = FakeAgent(simple_result("final answer"))
        agent._state["agent"] = fake
        assert run(agent.ask("q", session_id="s1")) == "final answer"
        assert fake.last_config["configurable"]["thread_id"] == "s1"
        assert captured_logs[0]["query"] == "q"
        assert captured_logs[0]["response_preview"] == "final answer"
        assert "s1" in agent._session_order

    def test_collects_tool_names_and_token_usage(self, captured_logs):
        messages = [
            HumanMessage(content="show flagged reviews"),
            ai_message("", tool_calls=[{"name": "flagged_reviews", "args": {}, "id": "1"}],
                       usage={"input_tokens": 3, "output_tokens": 2}),
            ai_message("done", usage={"input_tokens": 10, "output_tokens": 5}),
        ]
        agent._state["agent"] = FakeAgent({"messages": messages})
        run(agent.ask("show flagged reviews"))
        logged = captured_logs[0]
        assert logged["tool_calls"] == ["flagged_reviews"]
        assert logged["prompt_tokens"] == 13
        assert logged["completion_tokens"] == 7

    def test_tool_calls_from_earlier_turns_are_not_reported(self, captured_logs):
        messages = [
            HumanMessage(content="first"),
            ai_message("", tool_calls=[{"name": "old_tool", "args": {}, "id": "1"}]),
            HumanMessage(content="second"),
            ai_message("final"),
        ]
        agent._state["agent"] = FakeAgent({"messages": messages})
        run(agent.ask("second"))
        assert captured_logs[0]["tool_calls"] == []

    def test_token_usage_counts_only_the_current_turn(self, captured_logs):
        messages = [
            HumanMessage(content="first"),
            ai_message("old answer", usage={"input_tokens": 1000, "output_tokens": 500}),
            HumanMessage(content="second"),
            ai_message("final", usage={"input_tokens": 10, "output_tokens": 5}),
        ]
        agent._state["agent"] = FakeAgent({"messages": messages})
        run(agent.ask("second"))
        assert captured_logs[0]["prompt_tokens"] == 10
        assert captured_logs[0]["completion_tokens"] == 5

    def test_handles_a_history_with_no_human_message(self, captured_logs):
        agent._state["agent"] = FakeAgent({"messages": [ai_message("only ai")]})
        assert run(agent.ask("q")) == "only ai"

    def test_list_content_is_flattened_to_text(self, captured_logs):
        blocks = [{"type": "text", "text": "hi "}, {"type": "text", "text": "there"}]
        agent._state["agent"] = FakeAgent({"messages": [HumanMessage(content="q"), ai_message(blocks)]})
        assert run(agent.ask("q")) == "hi there"

    def test_transient_error_is_retried_once(self, captured_logs):
        fake = FakeAgent(RuntimeError("blip"), simple_result("recovered"))
        agent._state["agent"] = fake
        assert run(agent.ask("q")) == "recovered"
        assert fake.calls == 2

    def test_dead_connection_restarts_the_agent_then_retries(self, monkeypatch, captured_logs):
        dead = type(constants.CONNECTION_ERROR_NAMES[0], (Exception,), {})("pipe closed")
        agent._state["agent"] = FakeAgent(dead)
        replacement = FakeAgent(simple_result("from the new agent"))
        restarts = []

        async def fake_restart():
            restarts.append(True)
            agent._state["agent"] = replacement

        monkeypatch.setattr(agent, "_restart_agent", fake_restart)
        assert run(agent.ask("q")) == "from the new agent"
        assert restarts == [True]

    def test_timeout_becomes_agent_timeout_error(self):
        agent._state["agent"] = FakeAgent(asyncio.TimeoutError(), asyncio.TimeoutError())
        with pytest.raises(AgentTimeoutError):
            run(agent.ask("q"))

    def test_step_limit_becomes_agent_loop_error_without_retry(self):
        fake = FakeAgent(GraphRecursionError("too many steps"))
        agent._state["agent"] = fake
        with pytest.raises(AgentLoopError):
            run(agent.ask("q"))
        assert fake.calls == 1

    def test_provider_rate_limit_becomes_llm_rate_limit_error(self):
        limited = Exception("slow down")
        limited.status_code = 429
        fake = FakeAgent(limited, limited)
        agent._state["agent"] = fake
        with pytest.raises(LLMRateLimitError):
            run(agent.ask("q"))
        assert fake.calls == 2

    def test_unknown_failure_becomes_llm_service_error(self):
        agent._state["agent"] = FakeAgent(RuntimeError("a"), RuntimeError("b"))
        with pytest.raises(LLMServiceError):
            run(agent.ask("q"))

    def test_app_errors_are_passed_through_unchanged(self):
        agent._state["agent"] = FakeAgent(InvalidInputError("bad"), InvalidInputError("bad"))
        with pytest.raises(InvalidInputError):
            run(agent.ask("q"))


class TestRunCli:
    def test_asks_until_exit_and_always_shuts_down(self, monkeypatch):
        answers = iter(["first question", "exit"])
        asked, shutdowns = [], []

        async def fake_init():
            return None

        async def fake_ask(question, session_id=None):
            asked.append((question, session_id))
            return "an answer"

        async def fake_shutdown():
            shutdowns.append(True)

        monkeypatch.setattr(agent, "init_agent", fake_init)
        monkeypatch.setattr(agent, "ask", fake_ask)
        monkeypatch.setattr(agent, "shutdown_agent", fake_shutdown)
        monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))

        run(agent._run_cli())
        assert asked == [("first question", "cli-session")]
        assert shutdowns == [True]

    def test_an_app_error_does_not_end_the_loop(self, monkeypatch):
        answers = iter(["bad question", "exit"])
        shutdowns = []

        async def fake_init():
            return None

        async def failing_ask(question, session_id=None):
            raise AgentError("not running")

        async def fake_shutdown():
            shutdowns.append(True)

        monkeypatch.setattr(agent, "init_agent", fake_init)
        monkeypatch.setattr(agent, "ask", failing_ask)
        monkeypatch.setattr(agent, "shutdown_agent", fake_shutdown)
        monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))

        run(agent._run_cli())
        assert shutdowns == [True]

