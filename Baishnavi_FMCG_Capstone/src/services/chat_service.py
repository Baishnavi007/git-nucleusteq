"""
chat_service.py
====================
Thin service layer between chat_router.py and the agent: validates input,
enforces a simple per-session rate limit, and awaits the async ask()
directly (FastAPI already runs inside an event loop).
"""

import time
from collections import defaultdict, deque

from src.agents.agent import ask
from src.config import constants
from src.exceptions import InvalidInputError, RateLimitExceededError


_recent_calls = defaultdict(deque)


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


async def get_answer(question, session_id=constants.DEFAULT_SESSION_ID):
    """Runs one question through the agent and returns the final text answer."""
    if not question or not question.strip():
        raise InvalidInputError("The question cannot be empty.")
    _check_rate_limit(session_id)
    return await ask(question.strip(), session_id=session_id)
