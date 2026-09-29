"""Tests for src/services/chat_service.py: input validation and the
per-session rate limiter. The agent itself (ask()) is replaced with a
fake, so these run with no API key, no MCP server, and no network.
"""

import pytest

from src.config import constants
from src.exceptions import InvalidInputError
from src.services import chat_service


@pytest.fixture(autouse=True)
def clean_rate_limit_state():
    """chat_service keeps its rate-limit state at module level (a plain
    dict, not something the app resets between requests), so each test
    clears it first -- otherwise call counts would leak between tests."""
    chat_service._recent_calls.clear()
    yield
    chat_service._recent_calls.clear()


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
        with pytest.raises(InvalidInputError):
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
        fake_now["t"] += 61  # advance past the window
        chat_service._check_rate_limit("sessionE")  