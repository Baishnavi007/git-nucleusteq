"""Tests for the global exception handler (src/exceptions/custom_exceptions.py),
using a tiny throwaway FastAPI app rather than the real one, so these
tests don't need the agent, the dataset, or a Groq key.

Needs `httpx` installed (FastAPI's TestClient uses it under the hood).
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.config import constants
from src.exceptions import DataNotFoundError, InvalidInputError, register_exception_handlers


def make_client():
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/boom/app-error")
    def app_error():
        raise DataNotFoundError("no data here")

    @app.get("/boom/input-error")
    def input_error():
        raise InvalidInputError("bad input")

    @app.get("/boom/unexpected")
    def unexpected():
        raise RuntimeError("something broke internally")

    @app.get("/boom/http-error")
    def http_error():
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="not found here")

    @app.post("/echo")
    def echo(count: int):
        return {"count": count}

    return TestClient(app, raise_server_exceptions=False)


class TestAppErrorHandling:
    def test_status_code_comes_from_the_error(self):
        response = make_client().get("/boom/app-error")
        assert response.status_code == 404  # DataNotFoundError.status_code

    def test_body_has_the_error_shape(self):
        response = make_client().get("/boom/app-error")
        body = response.json()
        assert body["success"] is False
        assert body["error"]["code"] == constants.ERROR_CODE_DATA_NOT_FOUND
        assert body["message"] == "no data here"
        assert body["error"]["path"] == "/boom/app-error"

    def test_input_error_returns_400(self):
        response = make_client().get("/boom/input-error")
        assert response.status_code == 400
        assert response.json()["error"]["code"] == constants.ERROR_CODE_INVALID_INPUT

    def test_default_message_comes_from_constants(self):
        assert DataNotFoundError().message == constants.MSG_DATA_NOT_FOUND


class TestUnexpectedErrorHandling:
    def test_returns_500_with_a_generic_message(self):
        response = make_client().get("/boom/unexpected")
        assert response.status_code == 500
        body = response.json()
        assert body["error"]["code"] == constants.ERROR_CODE_INTERNAL
        assert body["message"] == constants.MSG_INTERNAL_ERROR

    def test_does_not_leak_the_real_exception_text(self):
        response = make_client().get("/boom/unexpected")
        body = response.json()
        assert "something broke internally" not in body["message"]


class TestHttpErrorHandling:
    def test_starlette_http_exception_is_wrapped_the_same_way(self):
        response = make_client().get("/boom/http-error")
        assert response.status_code == 404
        body = response.json()
        assert body["error"]["code"] == constants.ERROR_CODE_HTTP
        assert body["message"] == "not found here"


class TestValidationErrorHandling:
    def test_missing_required_field_returns_422(self):
        response = make_client().post("/echo", json={})
        assert response.status_code == 422
        body = response.json()
        assert body["error"]["code"] == constants.ERROR_CODE_VALIDATION
        assert body["error"]["details"]  