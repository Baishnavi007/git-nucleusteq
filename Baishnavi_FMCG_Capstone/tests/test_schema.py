"""Tests for the Pydantic request/response shapes in src/schemas/. These
exercise the validation Pydantic performs from the field constraints
(min_length, max_length) -- no FastAPI app needed.
"""

import pytest
from pydantic import ValidationError

from src.config import constants
from src.schemas.chat_schema import ChatMessage, ChatRequest
from src.schemas.response_schema import ChatResponse, DashboardSummaryResponse, HealthResponse


class TestChatRequest:
    def test_accepts_a_normal_question(self):
        request = ChatRequest(question="How's packaging?")
        assert request.question == "How's packaging?"
        assert request.session_id == constants.DEFAULT_SESSION_ID  # default applied

    def test_rejects_an_empty_question(self):
        with pytest.raises(ValidationError):
            ChatRequest(question="")

    def test_rejects_a_question_over_the_max_length(self):
        with pytest.raises(ValidationError):
            ChatRequest(question="x" * (constants.MAX_QUESTION_LENGTH + 1))

    def test_accepts_a_custom_session_id(self):
        request = ChatRequest(question="hi", session_id="my-session")
        assert request.session_id == "my-session"

    def test_rejects_a_session_id_over_the_max_length(self):
        with pytest.raises(ValidationError):
            ChatRequest(question="hi", session_id="x" * (constants.SESSION_ID_MAX_LENGTH + 1))


class TestChatMessage:
    def test_round_trips_role_and_content(self):
        message = ChatMessage(role="user", content="hello")
        assert message.role == "user"
        assert message.content == "hello"


class TestResponseSchemas:
    def test_chat_response(self):
        assert ChatResponse(answer="hi").answer == "hi"

    def test_health_response(self):
        assert HealthResponse(status="ok").status == "ok"

    def test_dashboard_summary_response_coerces_types(self):
        response = DashboardSummaryResponse(
            total_reviews="5", avg_rating="4.2", negative_pct="10.0", high_severity_count="1",
        )
        assert response.total_reviews == 5
        assert response.avg_rating == 4.2

    def test_dashboard_summary_response_requires_all_fields(self):
        with pytest.raises(ValidationError):
            DashboardSummaryResponse(total_reviews=5)