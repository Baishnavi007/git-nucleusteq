"""
dashboard_router.py
====================
Dashboard endpoints, backed by src/services/dashboard_service.py.

Query parameters are declared once as models in request_schema.py;
FastAPI uses their type hints to convert "2012-03-01" into a date and
"3" into an int.
"""

from typing import Annotated, Dict, List

from fastapi import APIRouter, Query

from src.config import constants
from src.schemas.request_schema import (
    DashboardFilterQuery,
    DateRangeQuery,
    FlaggedReviewsQuery,
    TopProductsQuery,
    UsageQuery,
)
from src.schemas.response_schema import (
    ApiResponse,
    DashboardSummaryResponse,
    DateRangeResponse,
    GenerateReportResponse,
    SentimentTrendResponse,
    UsageSummaryResponse,
    success_response,
)
from src.services.dashboard_service import (
    generate_report_now as _generate_report_now,
    get_aspect_breakdown as _get_aspect_breakdown,
    get_aspects as _get_aspects,
    get_column_metadata as _get_column_metadata,
    get_date_range as _get_date_range,
    get_flagged_reviews_view as _get_flagged_reviews_view,
    get_sentiment_trend as _get_sentiment_trend,
    get_summary as _get_summary,
    get_top_products as _get_top_products,
    get_usage_summary as _get_usage_summary,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/aspects", response_model=ApiResponse[List[str]])
def get_aspects():
    """Distinct aspect values, for populating filter dropdowns."""
    return success_response(_get_aspects())


@router.get("/column-metadata", response_model=ApiResponse[Dict[str, str]])
def get_column_metadata():
    """Plain-language description of each flagged-reviews column, for the
    dashboard's header tooltips. Wording follows DATASET_ITEM_LABEL."""
    return success_response(_get_column_metadata())


@router.get("/date-range", response_model=ApiResponse[DateRangeResponse])
def get_date_range():
    """First and last review dates in the dataset, for bounding the date pickers."""
    return success_response(_get_date_range())


@router.get("/summary", response_model=ApiResponse[DashboardSummaryResponse])
def get_summary(filters: Annotated[DashboardFilterQuery, Query()]):
    return success_response(_get_summary(filters.start_date, filters.end_date, filters.aspect))


@router.get("/sentiment-trend", response_model=ApiResponse[SentimentTrendResponse])
def get_sentiment_trend(filters: Annotated[DashboardFilterQuery, Query()]):
    return success_response(
        _get_sentiment_trend(filters.start_date, filters.end_date, filters.aspect)
    )


@router.get("/aspect-breakdown", response_model=ApiResponse[List[dict]])
def get_aspect_breakdown(filters: Annotated[DateRangeQuery, Query()]):
    return success_response(_get_aspect_breakdown(filters.start_date, filters.end_date))


@router.get("/top-products", response_model=ApiResponse[List[dict]])
def get_top_products(filters: Annotated[TopProductsQuery, Query()]):
    return success_response(
        _get_top_products(filters.start_date, filters.end_date, filters.limit)
    )


@router.get("/flagged-reviews", response_model=ApiResponse[List[dict]])
def get_flagged_reviews_view(filters: Annotated[FlaggedReviewsQuery, Query()]):
    return success_response(_get_flagged_reviews_view(
        filters.min_severity, filters.start_date, filters.end_date,
        filters.aspect, filters.search,
    ))


@router.post("/generate-report", response_model=ApiResponse[GenerateReportResponse])
async def generate_report():
    """Manually triggers one weekly brand-health report run -- the same
    code path as the scheduler and `python -m scripts.generate_sample_report`
    -- and returns the generated Markdown. Overwrites docs/sample_weekly_report.md
    and appends to docs/report_history.jsonl, same as any other run.
    """
    return success_response(await _generate_report_now(), constants.MSG_REPORT_GENERATED)


@router.get("/usage", response_model=ApiResponse[UsageSummaryResponse])
def get_usage_summary(params: Annotated[UsageQuery, Query()]):
    """Model usage: total calls, tokens, average latency, estimated cost
    (if COST_PER_1K_* is configured), and a per-day series for the chart."""
    return success_response(_get_usage_summary(params.days))
