"""
dashboard_router.py
====================
Dashboard endpoints, backed by src/services/dashboard_service.py.

The type hints on the query parameters are required here: FastAPI uses
them to convert "2012-03-01" into a date and "3" into an int.
"""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Query

from src.config import constants
from src.schemas.response_schema import DashboardSummaryResponse
from src.services.dashboard_service import (
    generate_report_now as _generate_report_now,
    get_aspect_breakdown as _get_aspect_breakdown,
    get_aspects as _get_aspects,
    get_date_range as _get_date_range,
    get_flagged_reviews_view as _get_flagged_reviews_view,
    get_sentiment_trend as _get_sentiment_trend,
    get_summary as _get_summary,
    get_top_products as _get_top_products,
    get_usage_summary as _get_usage_summary,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/aspects")
def get_aspects():
    """Distinct aspect values, for populating filter dropdowns."""
    return _get_aspects()


@router.get("/date-range")
def get_date_range():
    """First and last review dates in the dataset, for bounding the date pickers."""
    return _get_date_range()


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_summary(
    start_date: Optional[date] = Query(None, description="Filter start date"),
    end_date: Optional[date] = Query(None, description="Filter end date"),
    aspect: Optional[str] = Query(None, description="Filter to one aspect, e.g. 'packaging'"),
):
    return _get_summary(start_date, end_date, aspect)


@router.get("/sentiment-trend")
def get_sentiment_trend(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    aspect: Optional[str] = Query(None),
):
    return _get_sentiment_trend(start_date, end_date, aspect)


@router.get("/aspect-breakdown")
def get_aspect_breakdown(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
):
    return _get_aspect_breakdown(start_date, end_date)


@router.get("/top-products")
def get_top_products(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    limit: int = Query(constants.DASHBOARD_TOP_PRODUCTS_LIMIT, ge=1, le=constants.MAX_TOP_PRODUCTS_LIMIT),
):
    return _get_top_products(start_date, end_date, limit)


@router.get("/flagged-reviews")
def get_flagged_reviews_view(
    min_severity: int = Query(constants.DEFAULT_MIN_SEVERITY, ge=0, le=5),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    aspect: Optional[str] = Query(None),
    search: Optional[str] = Query(None, description="Free-text search over product/summary/text"),
):
    return _get_flagged_reviews_view(min_severity, start_date, end_date, aspect, search)


@router.post("/generate-report")
async def generate_report():
    """Manually triggers one weekly brand-health report run -- the same
    code path as the scheduler and `python -m scripts.generate_sample_report`
    -- and returns the generated Markdown. Overwrites docs/sample_weekly_report.md
    and appends to docs/report_history.jsonl, same as any other run.
    """
    return await _generate_report_now()


@router.get("/usage")
def get_usage_summary(days: int = Query(constants.USAGE_CHART_DAYS, ge=1, le=90)):
    """Model usage: total calls, tokens, average latency, estimated cost
    (if COST_PER_1K_* is configured), and a per-day series for the chart."""
    return _get_usage_summary(days)