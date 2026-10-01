"""Tests for the Pydantic request/response shapes in src/schemas/. These
exercise the validation Pydantic performs from the field constraints
(min_length, max_length) -- no FastAPI app needed.
"""

import pytest
from pydantic import ValidationError

from src.config import constants
from src.exceptions import InvalidInputError
from src.schemas.request_schema import (
    ChatRequest,
    DashboardFilterQuery,
    FlaggedReviewsQuery,
    FlaggedReviewsRequest,
    SearchReviewsRequest,
    SentimentTrendsRequest,
    validate_request,
)
from src.schemas.response_schema import (
    ChatMessage,
    ChatResponse,
    DashboardSummaryResponse,
    HealthResponse,
    error_response,
    success_response,
)


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


class TestEnvelope:
    def test_success_response_shape(self):
        body = success_response({"a": 1}, "done").model_dump()
        assert body["success"] is True
        assert body["message"] == "done"
        assert body["data"] == {"a": 1}
        assert body["error"] is None

    def test_error_response_shape(self):
        body = error_response("SOME_CODE", "bad", "/x", [{"field": "q"}]).model_dump()
        assert body["success"] is False
        assert body["message"] == "bad"
        assert body["data"] is None
        assert body["error"] == {"code": "SOME_CODE", "path": "/x", "details": [{"field": "q"}]}



class TestDashboardQueryModels:
    def test_start_after_end_is_rejected(self):
        with pytest.raises(ValidationError):
            DashboardFilterQuery(start_date="2013-02-01", end_date="2013-01-01")

    def test_filters_default_to_none(self):
        filters = DashboardFilterQuery()
        assert filters.start_date is None and filters.aspect is None

    def test_flagged_query_severity_bounds(self):
        with pytest.raises(ValidationError):
            FlaggedReviewsQuery(min_severity=99)
        assert FlaggedReviewsQuery().min_severity == constants.DEFAULT_MIN_SEVERITY


class TestToolRequestModels:
    def test_bad_aspect_becomes_invalid_input_error(self):
        with pytest.raises(InvalidInputError, match="aspect must be one of"):
            validate_request(SentimentTrendsRequest, aspect="nonsense")

    def test_bad_granularity_becomes_invalid_input_error(self):
        with pytest.raises(InvalidInputError, match="granularity"):
            validate_request(SentimentTrendsRequest, granularity="century")

    def test_severity_out_of_range(self):
        with pytest.raises(InvalidInputError, match="between 0 and 5"):
            validate_request(FlaggedReviewsRequest, min_severity=9)

    def test_limit_is_clamped_not_rejected(self):
        request = validate_request(FlaggedReviewsRequest, limit=10_000)
        assert request.limit == constants.MAX_FLAG_LIMIT

    def test_empty_search_query_rejected(self):
        with pytest.raises(InvalidInputError, match="query cannot be empty"):
            validate_request(SearchReviewsRequest, query="   ")

    def test_n_results_is_clamped(self):
        request = validate_request(SearchReviewsRequest, query="smell", n_results=0)
        assert request.n_results == 1
