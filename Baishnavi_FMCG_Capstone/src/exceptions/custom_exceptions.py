"""
custom_exceptions.py
====================
Every error this project raises on purpose. Each one carries the HTTP
status code and a short machine-readable code, so the global handler in
handlers.py can turn any of them into a clean JSON response without a
try/except in every route.
"""


class AppError(Exception):
    """Base class. Catch this to catch every deliberate project error."""

    status_code = 500
    error_code = "APP_ERROR"
    default_message = "Something went wrong."

    def __init__(self, message=None, details=None):
        self.message = message or self.default_message
        self.details = details
        super().__init__(self.message)


class ConfigError(AppError):
    status_code = 500
    error_code = "CONFIG_ERROR"
    default_message = "The application is not configured correctly."


class InvalidInputError(AppError):
    status_code = 400
    error_code = "INVALID_INPUT"
    default_message = "The request contains an invalid value."


class DataNotFoundError(AppError):
    status_code = 404
    error_code = "DATA_NOT_FOUND"
    default_message = "The requested data could not be found."


class VectorStoreError(AppError):
    status_code = 503
    error_code = "VECTORSTORE_UNAVAILABLE"
    default_message = "The review search index is not available."


class AgentError(AppError):
    status_code = 503
    error_code = "AGENT_UNAVAILABLE"
    default_message = "The review agent is not available right now."


class LLMServiceError(AppError):
    status_code = 502
    error_code = "LLM_SERVICE_ERROR"
    default_message = "The language model service failed to answer."


class LLMRateLimitError(AppError):
    status_code = 429
    error_code = "LLM_RATE_LIMIT"
    default_message = (
        "The question (plus the review data needed to answer it) was too "
        "large for the model provider's rate limit. Try a narrower "
        "question -- a shorter date range, one product, or fewer "
        "reviews -- or wait a minute and try again."
    )


class AgentTimeoutError(AppError):
    status_code = 504
    error_code = "AGENT_TIMEOUT"
    default_message = "The agent took too long to answer. Please try again."


class AgentLoopError(AppError):
    status_code = 422
    error_code = "AGENT_STEP_LIMIT"
    default_message = (
        "The agent could not find enough data to answer within the allowed "
        "number of steps. Try rephrasing or narrowing the question."
    )
