"""
sentiment_trends.py
====================
Tool 1: aggregates sentiment counts over time, optionally scoped to one
aspect (taste/packaging/price/availability/other) and/or one product.
"""

import pandas as pd

from src.config import constants
from src.exceptions import InvalidInputError
from src.repositories.data_access import filter_by_date, load_reviews
from src.utils.logger import get_logger

logger = get_logger(__name__)


def _resolve_product(df, product_id, product_name):
    """Applies product_id (exact) or product_name (substring, case-
    insensitive) filtering. Returns (filtered_df, warning_or_None)."""
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


def sentiment_trends(aspect=None, start_date=None, end_date=None,
                     granularity=constants.DEFAULT_GRANULARITY,
                     product_id=None, product_name=None):
    """
    Returns sentiment counts/percentages bucketed by time period, with the
    change from the previous period already computed -- the caller should
    report `negative_pct_change` rather than compute it itself, since a
    model computing period-over-period deltas from raw counts is a common
    source of arithmetic mistakes.

    Args:
        aspect: filter to one aspect. None = all. Must be one of
            constants.ASPECTS if given.
        start_date / end_date: ISO date strings. None = no bound.
        granularity: "day" | "week" | "month".
        product_id: filter to one exact ProductId. None = all products.
        product_name: filter to products whose name contains this text
            (case-insensitive substring match). If multiple distinct
            ProductIds share this name, a warning is included instead
            of silently merging unrelated products.
    """
    if aspect and aspect not in constants.ASPECTS:
        raise InvalidInputError(f"aspect must be one of {constants.ASPECTS}, got {aspect!r}")
    if granularity not in constants.GRANULARITY_FREQ:
        raise InvalidInputError(
            f"granularity must be one of {list(constants.GRANULARITY_FREQ)}, got {granularity!r}"
        )

    df = load_reviews()
    df = filter_by_date(df, start_date, end_date)
    if aspect:
        df = df[df["aspect"] == aspect]
    df, warning = _resolve_product(df, product_id, product_name)

    if df.empty:
        result = {
            "granularity": granularity, "aspect": aspect,
            "product_id": product_id, "product_name": product_name,
            "periods": [], "message": "No reviews found matching these filters.",
        }
        if warning:
            result["warning"] = warning
        return result

    freq = constants.GRANULARITY_FREQ[granularity]
    grouped = (
        df.groupby([pd.Grouper(key="datetime", freq=freq), "sentiment"])
        .size()
        .unstack(fill_value=0)
    )
    for column in constants.SENTIMENT_LABELS:
        if column not in grouped.columns:
            grouped[column] = 0

    grouped["total"] = grouped[list(constants.SENTIMENT_LABELS)].sum(axis=1)
    grouped["negative_pct"] = (grouped["negative"] / grouped["total"] * 100).round(1)
    grouped = grouped[grouped["total"] > 0]

    if len(grouped) > constants.TREND_MAX_PERIODS:
        logger.info("Trend has %s periods, truncating to the most recent %s",
                    len(grouped), constants.TREND_MAX_PERIODS)
        grouped = grouped.iloc[-constants.TREND_MAX_PERIODS:]

    prev_negative_pct = grouped["negative_pct"].shift(1)
    change = (grouped["negative_pct"] - prev_negative_pct).round(1)

    periods = [
        {
            "period": index.strftime("%Y-%m-%d"),
            "positive": int(row["positive"]),
            "neutral": int(row["neutral"]),
            "negative": int(row["negative"]),
            "total": int(row["total"]),
            "negative_pct": float(row["negative_pct"]),
            "negative_pct_change": None if pd.isna(change[index]) else float(change[index]),
        }
        for index, row in grouped.iterrows()
    ]

    result = {
        "granularity": granularity, "aspect": aspect,
        "product_id": product_id, "product_name": product_name,
        "periods": periods,
    }
    if warning:
        result["warning"] = warning
    return result
