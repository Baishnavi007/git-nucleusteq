"""
custom_exceptions.py
====================
Every error this project raises on purpose, plus the one global handler
and the function that registers it. Status codes, error codes and default
messages all live in src/config/constants.py.

register_exception_handlers(app) is called once from main.py; after that,
any error raised inside a request becomes the standard error envelope from
src/schemas/response_schema.py. Deliberate errors (AppError) show their own
message; anything unexpected is logged with its traceback but the client
only sees a generic message.
"""

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.config import constants
from src.schemas.response_schema import error_response
from src.utils.logger import get_logger

logger = get_logger(__name__)


class AppError(Exception):
    """Base class. Catch this to catch every deliberate project error."""

    status_code = constants.STATUS_INTERNAL_SERVER_ERROR
    error_code = constants.ERROR_CODE_APP
    default_message = constants.MSG_APP_ERROR

    def __init__(self, message=None, details=None):
        self.message = message or self.default_message
        self.details = details
        super().__init__(self.message)


class ConfigError(AppError):
    status_code = constants.STATUS_INTERNAL_SERVER_ERROR
    error_code = constants.ERROR_CODE_CONFIG
    default_message = constants.MSG_CONFIG_ERROR


class InvalidInputError(AppError):
    status_code = constants.STATUS_BAD_REQUEST
    error_code = constants.ERROR_CODE_INVALID_INPUT
    default_message = constants.MSG_INVALID_INPUT


class DataNotFoundError(AppError):
    status_code = constants.STATUS_NOT_FOUND
    error_code = constants.ERROR_CODE_DATA_NOT_FOUND
    default_message = constants.MSG_DATA_NOT_FOUND


class NoReviewsInRangeError(AppError):
    """A report was requested for a date range that has no reviews."""

    status_code = constants.STATUS_NOT_FOUND
    error_code = constants.ERROR_CODE_NO_REVIEWS_IN_RANGE
    default_message = constants.MSG_NO_REVIEWS_IN_RANGE


class RateLimitExceededError(AppError):
    status_code = constants.STATUS_TOO_MANY_REQUESTS
    error_code = constants.ERROR_CODE_RATE_LIMIT
    default_message = constants.MSG_RATE_LIMIT_EXCEEDED


class VectorStoreError(AppError):
    status_code = constants.STATUS_SERVICE_UNAVAILABLE
    error_code = constants.ERROR_CODE_VECTORSTORE
    default_message = constants.MSG_VECTORSTORE_UNAVAILABLE


class AgentError(AppError):
    status_code = constants.STATUS_SERVICE_UNAVAILABLE
    error_code = constants.ERROR_CODE_AGENT
    default_message = constants.MSG_AGENT_UNAVAILABLE


class LLMServiceError(AppError):
    status_code = constants.STATUS_BAD_GATEWAY
    error_code = constants.ERROR_CODE_LLM_SERVICE
    default_message = constants.MSG_LLM_SERVICE_ERROR


class LLMRateLimitError(AppError):
    status_code = constants.STATUS_TOO_MANY_REQUESTS
    error_code = constants.ERROR_CODE_LLM_RATE_LIMIT
    default_message = constants.MSG_LLM_RATE_LIMIT


class AgentTimeoutError(AppError):
    status_code = constants.STATUS_GATEWAY_TIMEOUT
    error_code = constants.ERROR_CODE_AGENT_TIMEOUT
    default_message = constants.MSG_AGENT_TIMEOUT


class AgentLoopError(AppError):
    status_code = constants.STATUS_UNPROCESSABLE_ENTITY
    error_code = constants.ERROR_CODE_AGENT_LOOP
    default_message = constants.MSG_AGENT_LOOP


async def handle_exception(request, error):
    """Turns any exception into the standard error envelope."""
    path = request.url.path
    details = None

    if isinstance(error, AppError):
        status_code, code = error.status_code, error.error_code
        message, details = error.message, error.details
    elif isinstance(error, RequestValidationError):
        status_code = constants.STATUS_UNPROCESSABLE_ENTITY
        code = constants.ERROR_CODE_VALIDATION
        message = constants.MSG_VALIDATION_ERROR
        details = [
            {"field": ".".join(str(part) for part in item["loc"]), "problem": item["msg"]}
            for item in error.errors()
        ]
    elif isinstance(error, StarletteHTTPException):
        status_code, code = error.status_code, constants.ERROR_CODE_HTTP
        message = str(error.detail)
    else:
        status_code = constants.STATUS_INTERNAL_SERVER_ERROR
        code = constants.ERROR_CODE_INTERNAL
        message = constants.MSG_INTERNAL_ERROR

    if code == constants.ERROR_CODE_INTERNAL:
        logger.exception("Unhandled error on %s", path)
    else:
        log = logger.error if status_code >= constants.SERVER_ERROR_MIN_STATUS else logger.warning
        log("%s on %s: %s", code, path, message)

    body = error_response(code, message, path, details)
    return JSONResponse(status_code=status_code, content=body.model_dump(exclude_none=True))


def register_exception_handlers(app):
    for exception_type in (AppError, RequestValidationError,
                           StarletteHTTPException, Exception):
        app.add_exception_handler(exception_type, handle_exception)

