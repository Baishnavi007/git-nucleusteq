"""
summary_report.py
====================
Tool 3: generates a period brand-health summary combining the sentiment
split, the per-aspect breakdown, a sentiment trend line and the top
flagged reviews. This is the tool behind the "generated sample weekly
brand-health report" deliverable -- see src/labeling's sibling script
scripts/generate_sample_report.py to write one to disk.
"""

from src.config import constants
from src.mcp.tools.flagged_reviews import flagged_reviews
from src.mcp.tools.sentiment_trends import sentiment_trends
from src.repositories.data_access import filter_by_date, load_reviews
from src.schemas.request_schema import SummaryReportRequest, validate_request
from src.utils.logger import get_logger

logger = get_logger(__name__)


def _resolve_product(df, product_id, product_name):
    if product_id:
        return df[df["ProductId"] == product_id], None
    if not product_name:
        return df, None

    matches = df[df["ProductName"].str.contains(product_name, case=False, na=False, regex=False)]
    distinct_ids = matches["ProductId"].unique()
    warning = None
    if len(distinct_ids) > 1:
        warning = (
            f"Note: '{product_name}' matches {len(distinct_ids)} different products "
            f"(ProductIds: {', '.join(sorted(distinct_ids))}). This summary combines "
            f"all of them. Ask by exact ProductId for a single specific product only."
        )
    return matches, warning


def summary_report(start_date=None, end_date=None, product_id=None, product_name=None):
    """
    Returns a structured brand-health summary: overall sentiment split,
    a sentiment trend line, negative share per aspect, and the top flagged
    (highest-severity) reviews in range -- optionally scoped to one product.

    Args:
        start_date / end_date: ISO date strings. None = no bound.
        product_id: scope the whole summary to one exact ProductId.
        product_name: scope the whole summary to products whose name
            contains this text (case-insensitive). If the name matches
            multiple distinct products, a warning is included in the
            result rather than silently combining them.
    """
    request = validate_request(
        SummaryReportRequest, start_date=start_date, end_date=end_date,
        product_id=product_id, product_name=product_name,
    )
    start_date, end_date = request.start_date, request.end_date
    product_id, product_name = request.product_id, request.product_name

    df = load_reviews()
    df = filter_by_date(df, start_date, end_date)
    df, warning = _resolve_product(df, product_id, product_name)

    total = len(df)
    if total == 0:
        result = {
            "date_range": {"start": start_date, "end": end_date},
            "product_id": product_id, "product_name": product_name,
            "message": "No reviews found matching these filters.",
        }
        if warning:
            result["warning"] = warning
        return result

    overall = {k: int(v) for k, v in df["sentiment"].value_counts().to_dict().items()}

    aspect_breakdown = {}
    for aspect in df["aspect"].dropna().unique():
        aspect_df = df[df["aspect"] == aspect]
        negative_pct = round((aspect_df["sentiment"] == "negative").mean() * 100, 1) if len(aspect_df) else 0.0
        aspect_breakdown[aspect] = {"count": int(len(aspect_df)), "negative_pct": negative_pct}

    trend = sentiment_trends(
        start_date=start_date, end_date=end_date, product_id=product_id,
        product_name=product_name, granularity=constants.SUMMARY_TREND_GRANULARITY,
    )
    trend_periods = trend.get("periods", [])[-constants.SUMMARY_TREND_MAX_PERIODS:]

    top_flags = flagged_reviews(
        min_severity=constants.HIGH_SEVERITY_THRESHOLD, start_date=start_date,
        end_date=end_date, product_id=product_id, product_name=product_name,
        limit=constants.SUMMARY_TOP_FLAGS,
    )

    result = {
        "date_range": {"start": start_date, "end": end_date},
        "product_id": product_id, "product_name": product_name,
        "total_reviews": total,
        "overall_sentiment": overall,
        "aspect_breakdown": aspect_breakdown,
        "sentiment_trend": trend_periods,
        "top_flagged_reviews": top_flags,
    }
    if warning:
        result["warning"] = warning

    logger.info("summary_report built for %s reviews", total)
    return result
