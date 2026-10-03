"""
flagged_reviews.py
====================
Tool 2: retrieves high-severity reviews for manual escalation. Answers
questions like "show me the high-severity flagged reviews from the last 7 days".
"""

from src.config import constants
from src.schemas.request_schema import FlaggedReviewsRequest, validate_request
from src.repositories.data_access import filter_by_date, load_reviews
from src.utils.guardrails import flag_suspicious_reviews
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
            f"(ProductIds: {', '.join(sorted(distinct_ids))}). Results below combine "
            f"all of them. Ask by exact ProductId for a single specific product only."
        )
    return matches, warning


def _truncate(text):
    if text is None:
        return text
    text = str(text)
    if len(text) <= constants.REVIEW_TEXT_MAX_CHARS:
        return text
    return text[:constants.REVIEW_TEXT_MAX_CHARS].rstrip() + "..."


def flagged_reviews(min_severity=constants.DEFAULT_MIN_SEVERITY, start_date=None,
                    end_date=None, aspect=None, product_id=None, product_name=None,
                    limit=constants.DEFAULT_FLAG_LIMIT):
    """
    Returns the highest-severity reviews matching the given filters,
    most severe and most recent first.

    Args:
        min_severity: minimum severity score to include (0-5 scale).
        start_date / end_date: ISO date strings (e.g. "2013-01-01"). None = no bound.
        aspect: filter to one aspect (e.g. "packaging"). None = all aspects.
        product_id: filter to one exact ProductId. None = all products.
        product_name: filter to products whose name contains this text
            (case-insensitive substring match). Some ProductNames cover
            multiple distinct ProductIds -- if that happens, a warning entry
            is included at the top of the results instead of silently
            merging unrelated products together.
        limit: max reviews to return (capped at constants.MAX_FLAG_LIMIT,
            default constants.DEFAULT_FLAG_LIMIT). Kept modest and each
            review's text truncated, because "give me all flagged reviews"
            can otherwise return enough text to exceed the model
            provider's per-request token limit in one tool call.

    Returns:
        [{"review_id": 123, "product_id": "...", "product_name": "...",
          "severity": 5, "sentiment": "negative", "aspect": "other",
          "date": "2013-01-05", "summary": "...", "text": "..."}, ...]
        If no matches: [{"message": "No reviews found matching these filters."}]
        If product_name is ambiguous: a {"warning": "..."} entry is prepended.
    """
    request = validate_request(
        FlaggedReviewsRequest, min_severity=min_severity, start_date=start_date,
        end_date=end_date, aspect=aspect, product_id=product_id,
        product_name=product_name, limit=limit,
    )

    df = load_reviews()
    df = filter_by_date(df, request.start_date, request.end_date)
    df = df[df["severity"] >= request.min_severity]
    if request.aspect:
        df = df[df["aspect"] == request.aspect]
    df, warning = _resolve_product(df, request.product_id, request.product_name)

    df = df.sort_values(["severity", "datetime"], ascending=[False, False]).head(request.limit)

    if df.empty:
        return [{"message": "No reviews found matching these filters."}]

    results = [
        {
            "review_id": int(row["Id"]),
            "product_name": row["ProductName"],
            "severity": int(row["severity"]),
            "sentiment": row["sentiment"],
            "aspect": row["aspect"],
            "date": row["datetime"].strftime("%Y-%m-%d"),
            "summary": _truncate(row["Summary"]),
            "text": _truncate(row["Text"]),
        }
        for _, row in df.iterrows()
    ]

    if warning:
        results.insert(0, {"warning": warning})
    results = flag_suspicious_reviews(
        results, text_fields=("summary", "text"),
        context_query=f"product_id={request.product_id}, product_name={request.product_name}",
    )
    logger.info("flagged_reviews returned %s item(s)", len(results))
    return results
