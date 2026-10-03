"""
chat_service.py
====================
Service layer between chat_router.py and the agent. It owns everything about
a chat session so the router stays a thin HTTP layer:
  * validates input and enforces a simple per-session rate limit
  * awaits the async ask() directly (FastAPI already runs inside an event loop)
  * keeps the per-session display history shown in the UI (capped at
    constants.CHAT_HISTORY_MAX_MESSAGES). This is a display log only -- the
    agent's own memory (agent.py, keyed by the same session_id) is what gives
    the model conversational context.
"""

import time
from collections import defaultdict, deque

from src.agents.agent import ask, clear_session
from src.config import constants
from src.exceptions import InvalidInputError, RateLimitExceededError


_recent_calls = defaultdict(deque)
_chat_history_by_session = {}


def _check_rate_limit(session_id):
    now = time.monotonic()
    window_start = now - constants.RATE_LIMIT_WINDOW_SECONDS
    calls = _recent_calls[session_id]
    while calls and calls[0] < window_start:
        calls.popleft()
    if len(calls) >= constants.CHAT_RATE_LIMIT_PER_MINUTE:
        raise RateLimitExceededError(
            f"Too many questions in a short time (limit: "
            f"{constants.CHAT_RATE_LIMIT_PER_MINUTE} per minute). Please wait a moment."
        )
    calls.append(now)


def _record_exchange(session_id, question, answer):
    """Stores one question/answer pair, keeping only the newest messages."""
    history = _chat_history_by_session.setdefault(session_id, [])
    history.append({"role": "user", "content": question})
    history.append({"role": "assistant", "content": answer})
    del history[: -constants.CHAT_HISTORY_MAX_MESSAGES]


def get_chat_history(session_id):
    """The display history for one session (empty list if there is none).
    Returns a copy, and does not create an entry for unknown sessions."""
    return list(_chat_history_by_session.get(session_id, []))


def clear_chat_history(session_id):
    """"Clear this chat": wipes the display history AND the agent's memory
    for that session, so the next question really starts fresh."""
    _chat_history_by_session.pop(session_id, None)
    clear_session(session_id)


async def get_answer(question, session_id=constants.DEFAULT_SESSION_ID):
    """Runs one question through the agent, records it in the session's
    history, and returns the final text answer."""
    if not question or not question.strip():
        raise InvalidInputError("The question cannot be empty.")
    _check_rate_limit(session_id)
    question = question.strip()
    answer = await ask(question, session_id=session_id)
    _record_exchange(session_id, question, answer)
    return answer
