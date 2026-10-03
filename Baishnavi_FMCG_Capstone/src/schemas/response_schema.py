"""
response_schema.py
====================
The ONE response shape every endpoint uses -- success and failure alike:

    success: {"success": true,  "message": "...", "data": <payload>}
    failure: {"success": false, "message": "...", "error": {"code": "...",
                                                            "path": "/x", "details": ...}}

Routers return success_response(payload); the global exception handler in
src/exceptions/custom_exceptions.py builds error_response(...). The
payload models below (ChatResponse, DashboardSummaryResponse, ...) are what
goes inside "data". Field annotations are required by Pydantic.
"""

from typing import Any, Generic, List, Optional, TypeVar

from pydantic import BaseModel

from src.config import constants

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    path: Optional[str] = None
    details: Optional[Any] = None


class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = constants.MSG_SUCCESS
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None


def success_response(data=None, message=constants.MSG_SUCCESS):
    return ApiResponse(success=True, message=message, data=data)


def error_response(code, message, path=None, details=None):
    return ApiResponse(
        success=False, message=message,
        error=ErrorDetail(code=code, path=path, details=details or None),
    )


# ---- payloads that go inside "data" ---------------------------------------

class ChatResponse(BaseModel):
    answer: str


class ChatMessage(BaseModel):
    role: str
    content: str


class ClearHistoryResponse(BaseModel):
    status: str
    session_id: str


class HealthResponse(BaseModel):
    status: str


class DashboardSummaryResponse(BaseModel):
    total_reviews: int
    avg_rating: float
    negative_pct: float
    high_severity_count: int


class DateRangeResponse(BaseModel):
    min_date: Optional[str] = None
    max_date: Optional[str] = None


class SentimentTrendResponse(BaseModel):
    split: dict = {}
    trend: List[dict] = []


class GenerateReportResponse(BaseModel):
    generated_at: str
    start_date: str
    end_date: str
    total_reviews: int
    report_markdown: str


class UsageSummaryResponse(BaseModel):
    total_calls: int
    total_prompt_tokens: int
    total_completion_tokens: int
    total_tokens: int
    avg_latency_ms: float
    estimated_cost_usd: Optional[float] = None
    cost_configured: bool
    daily: List[dict] = []
    recent_calls: List[dict] = []
