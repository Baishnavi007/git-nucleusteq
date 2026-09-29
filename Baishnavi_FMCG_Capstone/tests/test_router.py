"""Tests for the FastAPI routers (chat, dashboard, health), using a real
FastAPI app and TestClient with the service-layer functions replaced by
fakes. No agent, no dataset, no Groq key, no MCP servcer involved -- these
test routing, request validation, and response shape only.
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.exceptions import InvalidInputError
from src.exceptions.handlers import register_exception_handlers
from src.routers import chat_router, dashboard_router, health_router


@pytest.fixture(autouse=True)
def clean_chat_history():
    chat_router._chat_history_by_session.clear()
    yield
    chat_router._chat_history_by_session.clear()


def make_app():
    app = FastAPI()
    register_exception_handlers(app)
    app.include_router(health_router.router)
    app.include_router(chat_router.router)
    app.include_router(dashboard_router.router)
    return app


def make_client():
    return TestClient(make_app(), raise_server_exceptions=False)


class TestHealthRouter:
    def test_health_check_returns_ok(self):
        response = make_client().get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestChatRouterAsk:
    def test_valid_question_returns_the_answer(self, monkeypatch):
        async def fake_get_answer(question, session_id):
            return f"answer to: {question}"

        monkeypatch.setattr(chat_router, "get_answer", fake_get_answer)
        response = make_client().post("/chat/ask", json={"question": "How's packaging?"})
        assert response.status_code == 200
        assert response.json() == {"answer": "answer to: How's packaging?"}

    def test_empty_question_is_rejected_by_the_schema(self):
        response = make_client().post("/chat/ask", json={"question": ""})
        assert response.status_code == 422

    def test_missing_question_is_rejected(self):
        response = make_client().post("/chat/ask", json={})
        assert response.status_code == 422

    def test_service_error_becomes_a_clean_json_error(self, monkeypatch):
        async def failing_get_answer(question, session_id):
            raise InvalidInputError("too many questions")

        monkeypatch.setattr(chat_router, "get_answer", failing_get_answer)
        response = make_client().post("/chat/ask", json={"question": "hello"})
        assert response.status_code == 400
        assert response.json()["error"]["message"] == "too many questions"

    def test_successful_ask_is_recorded_in_history(self, monkeypatch):
        async def fake_get_answer(question, session_id):
            return "an answer"

        monkeypatch.setattr(chat_router, "get_answer", fake_get_answer)
        client = make_client()
        client.post("/chat/ask", json={"question": "q1", "session_id": "s1"})
        history = client.get("/chat/history", params={"session_id": "s1"}).json()
        assert [m["role"] for m in history] == ["user", "assistant"]

    def test_sessions_do_not_share_history(self, monkeypatch):
        async def fake_get_answer(question, session_id):
            return "an answer"

        monkeypatch.setattr(chat_router, "get_answer", fake_get_answer)
        client = make_client()
        client.post("/chat/ask", json={"question": "q1", "session_id": "s1"})
        other_history = client.get("/chat/history", params={"session_id": "s2"}).json()
        assert other_history == []


class TestChatRouterHistory:
    def test_clear_empties_that_sessions_history(self, monkeypatch):
        async def fake_get_answer(question, session_id):
            return "an answer"

        monkeypatch.setattr(chat_router, "get_answer", fake_get_answer)
        client = make_client()
        client.post("/chat/ask", json={"question": "q1", "session_id": "s1"})
        client.post("/chat/history/clear", params={"session_id": "s1"})
        assert client.get("/chat/history", params={"session_id": "s1"}).json() == []


class TestDashboardRouter:
    def test_aspects_returns_the_service_result(self, monkeypatch):
        monkeypatch.setattr(dashboard_router, "_get_aspects", lambda: ["taste", "packaging"])
        response = make_client().get("/dashboard/aspects")
        assert response.status_code == 200
        assert response.json() == ["taste", "packaging"]

    def test_summary_passes_query_params_through(self, monkeypatch):
        seen = {}

        def fake_get_summary(start_date, end_date, aspect):
            seen["args"] = (start_date, end_date, aspect)
            return {"total_reviews": 5, "avg_rating": 4.0, "negative_pct": 10.0, "high_severity_count": 1}

        monkeypatch.setattr(dashboard_router, "_get_summary", fake_get_summary)
        response = make_client().get(
            "/dashboard/summary",
            params={"start_date": "2013-01-01", "end_date": "2013-01-05", "aspect": "taste"},
        )
        assert response.status_code == 200
        assert response.json()["total_reviews"] == 5
        start, end, aspect = seen["args"]
        assert str(start) == "2013-01-01" and aspect == "taste"

    def test_top_products_limit_is_validated(self):
        # MAX_TOP_PRODUCTS_LIMIT caps this; a huge limit should be rejected.
        response = make_client().get("/dashboard/top-products", params={"limit": 10_000})
        assert response.status_code == 422

    def test_flagged_reviews_severity_out_of_range_is_rejected(self):
        response = make_client().get("/dashboard/flagged-reviews", params={"min_severity": 99})
        assert response.status_code == 422

    def test_usage_passes_days_through(self, monkeypatch):
        monkeypatch.setattr(dashboard_router, "_get_usage_summary", lambda days: {"total_calls": days})
        response = make_client().get("/dashboard/usage", params={"days": 7})
        assert response.json() == {"total_calls": 7}