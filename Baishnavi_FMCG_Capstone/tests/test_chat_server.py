"""Tests for src/services/chat_service.py: input validation and the
per-session rate limiter. The agent itself (ask()) is replaced with a
fake, so these run with no API key, no MCP server, and no network.
"""

import pytest

from src.config import constants
from src.exceptions import InvalidInputError, RateLimitExceededError
from src.services import chat_service


@pytest.fixture(autouse=True)
def clean_rate_limit_state():
    """chat_service keeps its rate-limit state at module level (a plain
    dict, not something the app resets between requests), so each test
    clears it first -- otherwise call counts would leak between tests."""
    chat_service._recent_calls.clear()
    chat_service._chat_history_by_session.clear()
    yield
    chat_service._recent_calls.clear()
    chat_service._chat_history_by_session.clear()


class TestGetAnswerValidation:
    def test_empty_question_is_rejected(self):
        with pytest.raises(InvalidInputError):
            import asyncio
            asyncio.run(chat_service.get_answer(""))

    def test_whitespace_only_question_is_rejected(self):
        import asyncio
        with pytest.raises(InvalidInputError):
            asyncio.run(chat_service.get_answer("   "))

    def test_valid_question_is_forwarded_to_the_agent(self, monkeypatch):
        import asyncio
        seen = {}

        async def fake_ask(question, session_id):
            seen["question"] = question
            seen["session_id"] = session_id
            return "the answer"

        monkeypatch.setattr(chat_service, "ask", fake_ask)
        answer = asyncio.run(chat_service.get_answer("  What about packaging?  ", session_id="s1"))
        assert answer == "the answer"
        assert seen == {"question": "What about packaging?", "session_id": "s1"}  # stripped


class TestRateLimit:
    def test_allows_calls_under_the_limit(self, monkeypatch):
        monkeypatch.setattr(constants, "CHAT_RATE_LIMIT_PER_MINUTE", 3)
        for _ in range(3):
            chat_service._check_rate_limit("sessionA")  # should not raise

    def test_blocks_the_call_over_the_limit(self, monkeypatch):
        monkeypatch.setattr(constants, "CHAT_RATE_LIMIT_PER_MINUTE", 2)
        chat_service._check_rate_limit("sessionB")
        chat_service._check_rate_limit("sessionB")
        with pytest.raises(RateLimitExceededError):
            chat_service._check_rate_limit("sessionB")

    def test_sessions_are_tracked_independently(self, monkeypatch):
        monkeypatch.setattr(constants, "CHAT_RATE_LIMIT_PER_MINUTE", 1)
        chat_service._check_rate_limit("sessionC")
        chat_service._check_rate_limit("sessionD")  # different session, own budget

    def test_old_calls_fall_outside_the_window(self, monkeypatch):
        monkeypatch.setattr(constants, "CHAT_RATE_LIMIT_PER_MINUTE", 1)
        monkeypatch.setattr(constants, "RATE_LIMIT_WINDOW_SECONDS", 60)

        import time
        fake_now = {"t": time.monotonic()}
        monkeypatch.setattr(chat_service.time, "monotonic", lambda: fake_now["t"])

        chat_service._check_rate_limit("sessionE")
        fake_now["t"] += 61  
        chat_service._check_rate_limit("sessionE")  

class TestChatHistory:
    def _ask(self, monkeypatch, question="hello", session_id="s1", answer="an answer"):
        import asyncio

        async def fake_ask(question, session_id):
            return answer

        monkeypatch.setattr(chat_service, "ask", fake_ask)
        return asyncio.run(chat_service.get_answer(question, session_id=session_id))

    def test_an_answered_question_is_stored_as_user_then_assistant(self, monkeypatch):
        self._ask(monkeypatch, question="  hello  ", answer="hi there")
        assert chat_service.get_chat_history("s1") == [
            {"role": "user", "content": "hello"},      # stripped, like the agent sees it
            {"role": "assistant", "content": "hi there"},
        ]

    def test_a_failed_question_is_not_stored(self, monkeypatch):
        import asyncio

        async def failing_ask(question, session_id):
            raise RuntimeError("model down")

        monkeypatch.setattr(chat_service, "ask", failing_ask)
        with pytest.raises(RuntimeError):
            asyncio.run(chat_service.get_answer("hello", session_id="s1"))
        assert chat_service.get_chat_history("s1") == []

    def test_history_keeps_only_the_newest_messages(self, monkeypatch):
        monkeypatch.setattr(constants, "CHAT_HISTORY_MAX_MESSAGES", 4)
        monkeypatch.setattr(constants, "CHAT_RATE_LIMIT_PER_MINUTE", 100)
        for number in range(5):
            self._ask(monkeypatch, question=f"q{number}", answer=f"a{number}")
        history = chat_service.get_chat_history("s1")
        assert [m["content"] for m in history] == ["q3", "a3", "q4", "a4"]

    def test_unknown_session_returns_empty_without_creating_an_entry(self):
        assert chat_service.get_chat_history("nobody") == []
        assert "nobody" not in chat_service._chat_history_by_session

    def test_returned_history_is_a_copy(self, monkeypatch):
        self._ask(monkeypatch)
        chat_service.get_chat_history("s1").clear()
        assert len(chat_service.get_chat_history("s1")) == 2

    def test_clearing_wipes_the_display_log_and_the_agent_memory(self, monkeypatch):
        self._ask(monkeypatch, session_id="s1")
        self._ask(monkeypatch, session_id="s2")
        cleared = []
        monkeypatch.setattr(chat_service, "clear_session", cleared.append)
        chat_service.clear_chat_history("s1")
        assert chat_service.get_chat_history("s1") == []
        assert cleared == ["s1"]                                  # agent memory too
        assert len(chat_service.get_chat_history("s2")) == 2      # other session untouched

