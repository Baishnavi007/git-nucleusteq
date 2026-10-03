"""
request_schema.py
====================
The ONE place every input to the project is described and validated.

  1. HTTP requests (FastAPI): ChatRequest, SessionQuery and the dashboard
     query models. Routers declare them once, e.g.
         filters: Annotated[DashboardFilterQuery, Query()]
     instead of re-typing start_date / end_date / aspect on every endpoint.
     Needs fastapi>=0.115 (Pydantic models as query parameters).

  2. MCP tool arguments: the four *Request models. server.py must keep its
     flat function signatures (the LLM reads them), so each tool calls
         request = validate_request(FlaggedReviewsRequest, **arguments)
     which applies the same rules everywhere and raises InvalidInputError.

Allowed values (aspects, sentiments...) and messages come from constants.py.
"""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

from src.config import constants
from src.exceptions import InvalidInputError


# ---------------------------------------------------------------------------
# 1. HTTP requests
# ---------------------------------------------------------------------------

class SessionQuery(BaseModel):
    session_id: str = Field(
        default=constants.DEFAULT_SESSION_ID, max_length=constants.SESSION_ID_MAX_LENGTH,
        description="Identifies one conversation so follow-up questions keep context. "
                    "Generate one random ID per browser session and reuse it.",
    )


class ChatRequest(SessionQuery):
    question: str = Field(
        ..., min_length=1, max_length=constants.MAX_QUESTION_LENGTH,
        description="A natural-language question about customer reviews.",
    )


class DateRangeQuery(BaseModel):
    start_date: Optional[date] = Field(None, description="Filter start date")
    end_date: Optional[date] = Field(None, description="Filter end date")

    @model_validator(mode="after")
    def _start_not_after_end(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError(constants.MSG_START_AFTER_END)
        return self


class DashboardFilterQuery(DateRangeQuery):
    aspect: Optional[str] = Field(None, description="Filter to one aspect, e.g. 'packaging'")


class TopProductsQuery(DateRangeQuery):
    limit: int = Field(constants.DASHBOARD_TOP_PRODUCTS_LIMIT, ge=1, le=constants.MAX_TOP_PRODUCTS_LIMIT)


class FlaggedReviewsQuery(DashboardFilterQuery):
    min_severity: int = Field(
        constants.DEFAULT_MIN_SEVERITY, ge=constants.SEVERITY_MIN, le=constants.SEVERITY_MAX,
    )
    search: Optional[str] = Field(None, description="Free-text search over product/summary/text")
    limit: int = Field(
        constants.DASHBOARD_FLAGGED_LIMIT, ge=1, le=constants.MAX_DASHBOARD_FLAGGED_LIMIT,
        description="Max rows returned, most severe first",
    )


class UsageQuery(BaseModel):
    days: int = Field(constants.USAGE_CHART_DAYS, ge=1, le=90)


# ---------------------------------------------------------------------------
# 2. MCP tool arguments
# ---------------------------------------------------------------------------

class ProductDateFilter(BaseModel):
    start_date: Optional[str] = None   # ISO date string; parsed by data_access.filter_by_date
    end_date: Optional[str] = None
    product_id: Optional[str] = None
    product_name: Optional[str] = None


class ReviewFilterRequest(ProductDateFilter):
    aspect: Optional[str] = None

    @field_validator("aspect")
    @classmethod
    def _aspect_allowed(cls, value):
        if value and value not in constants.ASPECTS:
            raise ValueError(constants.MSG_INVALID_ASPECT.format(allowed=constants.ASPECTS, value=value))
        return value


class SentimentTrendsRequest(ReviewFilterRequest):
    granularity: str = constants.DEFAULT_GRANULARITY

    @field_validator("granularity")
    @classmethod
    def _granularity_allowed(cls, value):
        if value not in constants.GRANULARITY_FREQ:
            raise ValueError(constants.MSG_INVALID_GRANULARITY.format(
                allowed=list(constants.GRANULARITY_FREQ), value=value))
        return value


class FlaggedReviewsRequest(ReviewFilterRequest):
    min_severity: int = constants.DEFAULT_MIN_SEVERITY
    limit: int = constants.DEFAULT_FLAG_LIMIT

    @field_validator("min_severity")
    @classmethod
    def _severity_in_range(cls, value):
        if not constants.SEVERITY_MIN <= value <= constants.SEVERITY_MAX:
            raise ValueError(constants.MSG_INVALID_SEVERITY.format(
                low=constants.SEVERITY_MIN, high=constants.SEVERITY_MAX))
        return value

    @field_validator("limit")
    @classmethod
    def _clamp_limit(cls, value):
        return max(1, min(value, constants.MAX_FLAG_LIMIT))


class SummaryReportRequest(ProductDateFilter):
    pass


class SearchReviewsRequest(ReviewFilterRequest):
    query: str
    sentiment: Optional[str] = None
    min_severity: Optional[int] = None
    n_results: int = constants.SEARCH_DEFAULT_RESULTS

    @field_validator("query")
    @classmethod
    def _query_not_empty(cls, value):
        if not value or not value.strip():
            raise ValueError(constants.MSG_EMPTY_QUERY)
        return value

    @field_validator("sentiment")
    @classmethod
    def _sentiment_allowed(cls, value):
        if value and value not in constants.SENTIMENT_LABELS:
            raise ValueError(constants.MSG_INVALID_SENTIMENT.format(
                allowed=constants.SENTIMENT_LABELS, value=value))
        return value

    @field_validator("n_results")
    @classmethod
    def _clamp_n_results(cls, value):
        return max(1, min(value, constants.MAX_SEARCH_RESULTS))


def validate_request(model_class, **arguments):
    """Builds a request model from plain arguments; any rule violation
    becomes an InvalidInputError, so callers handle one exception type."""
    try:
        return model_class(**arguments)
    except ValidationError as error:
        first = error.errors()[0]
        message = str(first["msg"])
        if first["type"] == "value_error":
            message = message.removeprefix("Value error, ")
        else:
            message = f"{'.'.join(str(part) for part in first['loc'])}: {message}"
        details = [{"field": ".".join(str(part) for part in item["loc"]), "problem": item["msg"]}
                   for item in error.errors()]
        raise InvalidInputError(message, details) from error

