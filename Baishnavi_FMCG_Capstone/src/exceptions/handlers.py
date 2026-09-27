"""
handlers.py
====================
The global exception handler. register_exception_handlers(app) is called
once from main.py; after that, any error raised anywhere inside a request
becomes the same JSON shape:

    {"error": {"code": "...", "message": "...", "path": "/chat/ask"}}

Deliberate errors (AppError) show their own message. Anything unexpected
is logged in full with its traceback, but the client only sees a generic
message -- internal details never leak out.
"""

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.exceptions.custom_exceptions import AppError
from src.utils.logger import get_logger

logger = get_logger(__name__)

UNEXPECTED_ERROR_CODE = "INTERNAL_ERROR"
UNEXPECTED_ERROR_MESSAGE = "An unexpected error occurred. Please try again."


def build_error_response(status_code, error_code, message, path, details=None):
    body = {"error": {"code": error_code, "message": message, "path": path}}
    if details:
        body["error"]["details"] = details
    return JSONResponse(status_code=status_code, content=body)


async def handle_app_error(request, error):
    log = logger.error if error.status_code >= 500 else logger.warning
    log("%s on %s: %s", error.error_code, request.url.path, error.message)
    return build_error_response(
        error.status_code, error.error_code, error.message,
        request.url.path, error.details,
    )


async def handle_validation_error(request, error):
    problems = [
        {"field": ".".join(str(part) for part in item["loc"]), "problem": item["msg"]}
        for item in error.errors()
    ]
    logger.warning("Validation failed on %s: %s", request.url.path, problems)
    return build_error_response(
        422, "VALIDATION_ERROR", "The request data is not valid.",
        request.url.path, problems,
    )


async def handle_http_error(request, error):
    logger.warning("HTTP %s on %s: %s", error.status_code, request.url.path, error.detail)
    return build_error_response(
        error.status_code, "HTTP_ERROR", str(error.detail), request.url.path,
    )


async def handle_unexpected_error(request, error):
    logger.exception("Unhandled error on %s", request.url.path)
    return build_error_response(
        500, UNEXPECTED_ERROR_CODE, UNEXPECTED_ERROR_MESSAGE, request.url.path,
    )


def register_exception_handlers(app):
    app.add_exception_handler(AppError, handle_app_error)
    app.add_exception_handler(RequestValidationError, handle_validation_error)
    app.add_exception_handler(StarletteHTTPException, handle_http_error)
    app.add_exception_handler(Exception, handle_unexpected_error)
