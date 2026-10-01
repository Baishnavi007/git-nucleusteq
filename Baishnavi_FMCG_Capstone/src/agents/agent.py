"""
agent.py
====================
Production agent: LangGraph + a Groq-hosted model, connected to the four
review-intelligence tools over the real MCP protocol. This file is the MCP
CLIENT; it starts src/mcp/server.py as a subprocess and keeps ONE session
open for the app's lifetime, so the embedding model loads once instead of
on every tool call.

Conversation memory: each caller passes a `session_id`; LangGraph's
MemorySaver checkpointer keeps that session's message history so follow-up
questions ("what about price?") have context. Sessions are capped
(constants.CHAT_MAX_SESSIONS) so the number of tracked conversations
doesn't grow unbounded; very long individual conversations still add to
each call's token usage, which is a reasonable trade for keeping context.

main.py calls init_agent() / shutdown_agent() from the FastAPI lifespan.

Manual test from the project root:
    python -m src.agents.agent
"""

import asyncio
import sys
from contextlib import AsyncExitStack
from datetime import date

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.checkpoint.memory import MemorySaver
from langgraph.errors import GraphRecursionError
from langgraph.prebuilt import create_react_agent




from src.config import constants
from src.config.prompts import AGENT_SYSTEM_PROMPT_TEMPLATE
from src.exceptions import (
    AgentError,
    AgentLoopError,
    AgentTimeoutError,
    AppError,
    LLMRateLimitError,
    LLMServiceError,
)
from src.repositories.data_access import get_dataset_today
from src.utils.llm_logger import Timer, log_call
from src.utils.logger import get_logger

logger = get_logger(__name__)

_state = {"agent": None, "stack": None, "system_prompt": None}
_init_lock = asyncio.Lock()
_session_order = []  # oldest-first list of session_ids seen, for capping


def build_system_prompt():
    """Anchors 'today' to the most recent date in the dataset, falling back
    to the real date if the dataset can't be read (e.g. before the data
    pipeline has run) so the agent can still start."""
    try:
        today = get_dataset_today()
    except AppError:
        logger.warning("Could not read dataset date range; falling back to the real date")
        today = date.today()
    return AGENT_SYSTEM_PROMPT_TEMPLATE.format(dataset_today=today.isoformat())


def _is_connection_error(error):
    return type(error).__name__ in constants.CONNECTION_ERROR_NAMES


def _is_rate_limit_error(error):
    """Detects a Groq (or OpenAI-style) 'request too large for your rate
    limit' response, wherever it surfaces in the exception chain -- the
    ReAct graph may wrap the original groq.APIStatusError."""
    seen = set()
    current = error
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        status_code = getattr(current, "status_code", None)
        if status_code in constants.PROVIDER_RATE_LIMIT_STATUSES:
            return True
        if "rate_limit_exceeded" in str(current) or "tokens per minute" in str(current):
            return True
        current = current.__cause__ or current.__context__
    return False


def _trim_for_model(messages):
    """Keeps only the most recent constants.AGENT_HISTORY_TURNS human turns
    (and everything that followed each, including tool calls/results),
    rather than resending the whole conversation every call. Full history
    still lives in the checkpointer for later use; this only shrinks what
    is actually sent to the model.

    Never cuts an AIMessage with tool_calls apart from its ToolMessage
    replies -- an orphaned tool_calls entry with no matching ToolMessage is
    rejected by the Groq/OpenAI-style chat API, so trimming always starts
    at a HumanMessage boundary.
    """
    human_positions = [i for i, message in enumerate(messages) if isinstance(message, HumanMessage)]
    if len(human_positions) <= constants.AGENT_HISTORY_TURNS:
        return messages
    start = human_positions[-constants.AGENT_HISTORY_TURNS]
    return messages[start:]


def _pre_model_hook(state):
    """create_react_agent calls this before each model call; returning
    llm_input_messages sends only the trimmed list to the model while
    leaving the full history in the checkpointed state untouched."""
    return {"llm_input_messages": _trim_for_model(state["messages"])}


async def _build_agent():
    stack = AsyncExitStack()
    client = MultiServerMCPClient({
        constants.MCP_SERVER_NAME: {
            "command": sys.executable,
            "args": ["-m", constants.MCP_SERVER_MODULE],
            "transport": constants.MCP_TRANSPORT,
            "cwd": str(constants.PROJECT_ROOT),
        }
    })
    session = await stack.enter_async_context(client.session(constants.MCP_SERVER_NAME))
    tools = await load_mcp_tools(session)
    llm = ChatGroq(
        model=constants.AGENT_MODEL_NAME,
        temperature=0,
        max_tokens=constants.AGENT_MAX_TOKENS,
    )
    llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)
    base_system_prompt = build_system_prompt()
    formatting_instructions = (
        "\n\nCRITICAL SYSTEM RULES FOR TOOL USE:\n"
        "1. When you want to call a function/tool, you MUST invoke it natively using the designated tool-calling mechanism.\n"
        "2. NEVER format or output tool calls manually inside your text response using XML tags like <tool_call>, <function>, or <parameter>.\n"
        "3. Do not invent or hallucinate input parameters that do not exist in the tool schemas."
        
    )
    final_system_prompt = base_system_prompt + formatting_instructions
    agent = create_react_agent(
        llm_with_tools, tools, prompt=final_system_prompt, checkpointer=MemorySaver(),
        pre_model_hook=_pre_model_hook,
    )
    return agent, stack, final_system_prompt, len(tools)


async def init_agent():
    """Starts the MCP server subprocess and builds the agent. Safe to call
    more than once -- a later call returns the agent already built."""
    async with _init_lock:
        if _state["agent"] is not None:
            return _state["agent"]

        logger.info("Starting agent (model=%s)", constants.AGENT_MODEL_NAME)
        try:
            agent, stack, system_prompt, tool_count = await _build_agent()
        except Exception as error:
            logger.exception("Agent start-up failed")
            raise AgentError("The review agent could not be started.") from error

        _state.update(agent=agent, stack=stack, system_prompt=system_prompt)
        logger.info("Agent ready with %s MCP tools. Today anchored to dataset max date.", tool_count)
        return agent


async def _restart_agent():
    """Rebuilds the agent and MCP session after the subprocess/session died.
    Existing conversation memory is lost on restart (MemorySaver is
    in-process); this trades a rare loss of history for staying available
    instead of erroring on every question until a manual restart."""
    logger.warning("Restarting agent after a dead MCP connection")
    old_stack = _state["stack"]
    _state.update(agent=None, stack=None)
    if old_stack is not None:
        try:
            await old_stack.aclose()
        except Exception:
            pass  # the connection is already broken; nothing more to clean up
    return await init_agent()


async def shutdown_agent():
    """Closes the MCP session and stops the server subprocess."""
    stack = _state["stack"]
    _state.update(agent=None, stack=None)
    if stack is None:
        return
    try:
        await asyncio.wait_for(stack.aclose(), timeout=constants.AGENT_STOP_TIMEOUT_SECONDS)
        logger.info("Agent stopped")
    except asyncio.TimeoutError:
        logger.warning("Agent shutdown timed out; the MCP subprocess may need to be killed manually")
    except Exception:
        logger.exception("Error while stopping the agent")


def _extract_text(content):
    """Model content is normally a string but can be a list of blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "".join(parts)
    return str(content)


def _track_session(session_id):
    """Keeps an oldest-first list of session_ids so the checkpointer's
    in-memory history doesn't grow forever. MemorySaver has no per-thread
    eviction API, so this is an approximate cap: it stops the *list* from
    growing past the limit and logs when older sessions age out; actual
    memory is bounded by AGENT_HISTORY_MESSAGES trimming each turn."""
    if session_id in _session_order:
        _session_order.remove(session_id)
    _session_order.append(session_id)
    if len(_session_order) > constants.CHAT_MAX_SESSIONS:
        dropped = _session_order.pop(0)
        logger.info("Session cap reached (%s); oldest session %r aged out of tracking",
                    constants.CHAT_MAX_SESSIONS, dropped)


async def ask(query, session_id=constants.DEFAULT_SESSION_ID):
    """Runs one query through the agent for the given conversation session,
    logs tokens/latency/tool calls, and returns the final text answer.
    Raises a subclass of AppError on failure."""
    if _state["agent"] is None:
        raise AgentError("The review agent is not running.")

    _track_session(session_id)
    payload = {"messages": [{"role": "user", "content": query}]}
    config = {
        "recursion_limit": constants.AGENT_RECURSION_LIMIT,
        "configurable": {"thread_id": session_id},
    }

    async def _invoke_once():
        return await asyncio.wait_for(
            _state["agent"].ainvoke(payload, config=config),
            timeout=constants.AGENT_TIMEOUT_SECONDS,
        )

    try:
        with Timer() as timer:
            max_attempts = 2
            for attempt in range(max_attempts):
                try:
                    result = await _invoke_once()
                    break
                except Exception as error:
                    if attempt == max_attempts -1 or isinstance(error, GraphRecursionError):
                        raise
                    
                    if _is_connection_error(error):
                        logger.warning("MCP connection appears dead; restarting environment instance once...")
                        await _restart_agent()
                    else:
                        logger.warning("Transient runtime or rate-limit anomaly detected. Retrying behind the scenes...")
                        await asyncio.sleep(1)
    except asyncio.TimeoutError as error:
        logger.error("Agent timed out after %ss for query: %r", constants.AGENT_TIMEOUT_SECONDS, query)
        raise AgentTimeoutError() from error
    except GraphRecursionError as error:
        logger.warning("Agent hit the step limit (%s) for query: %r", constants.AGENT_RECURSION_LIMIT, query)
        raise AgentLoopError() from error
    except AppError:
        raise
    except Exception as error:
        if _is_rate_limit_error(error):
            logger.warning("Model provider rate limit hit for query: %r (%s)", query, error)
            raise LLMRateLimitError() from error
        logger.exception("Agent call failed for query: %r", query)
        raise LLMServiceError() from error
      
    messages = result["messages"]
    final_text = _extract_text(messages[-1].content)
    human_positions = [i for i, msg in enumerate(messages) if isinstance(msg, HumanMessage)]
    current_turn_messages = messages[human_positions[-1]:] if human_positions else messages
    tool_calls_made = [
        call["name"]
        for message in current_turn_messages
        if hasattr(message, "tool_calls") and message.tool_calls
        for call in message.tool_calls
    ]

    prompt_tokens = completion_tokens = 0
    for message in messages:
        usage = getattr(message, "usage_metadata", None)
        if usage:
            prompt_tokens += usage.get("input_tokens", 0)
            completion_tokens += usage.get("output_tokens", 0)

    log_call(
        framework=f"production::langgraph::{constants.AGENT_MODEL_NAME}",
        query=query, tool_calls=tool_calls_made,
        prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
        latency_ms=timer.elapsed_ms, response_preview=final_text,
    )
    logger.info("[%s] answered in %.0f ms using tools: %s", session_id, timer.elapsed_ms, tool_calls_made or "none")
    return final_text


async def _run_cli():
    """Interactive test loop, all in one session so follow-up questions
    keep context."""
    await init_agent()
    session_id = "cli-session"
    try:
        logger.info("Agent ready. Model: %s. Type 'exit' to quit.", constants.AGENT_MODEL_NAME)
        while True:
            question = await asyncio.to_thread(input, "\nAsk a question (or 'exit'): ")
            if question.strip().lower() == "exit":
                break
            try:
                answer = await ask(question, session_id=session_id)
                logger.info("Answer:\n%s", answer)
            except AppError as error:
                logger.error("Could not answer: %s", error.message)
    finally:
        await shutdown_agent()


if __name__ == "__main__":
    asyncio.run(_run_cli())
