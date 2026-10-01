"""
dashboard_service.py
====================
Dashboard computations, returning plain dicts/lists so dashboard_router.py
can serve them over HTTP. Reads the same data (and the same date-filtering
rule) as the tools, through repositories/data_access.py, so the dashboard
and the chat agent never disagree about which reviews are "in range".
"""

import asyncio
from datetime import datetime, timezone

from src.config import constants
from src.exceptions import DataNotFoundError
from src.repositories.data_access import filter_by_date, load_reviews
from src.services.report_scheduler import run_report_once
from src.utils.llm_logger import summarize_usage


def _filtered(start_date=None, end_date=None, aspect=None):
    df = load_reviews()
    df = filter_by_date(df, start_date, end_date)
    if aspect:
        df = df[df["aspect"] == aspect]
    return df


def get_aspects():
    """Distinct aspect values, for the dashboard's filter dropdown."""
    df = load_reviews()
    return sorted(df["aspect"].dropna().unique().tolist())


def get_column_metadata():
    """Tooltip text for each flagged-reviews column. The wording comes from
    constants.COLUMN_DESCRIPTION_TEMPLATES filled with the configured dataset
    label and the aspect values found in the loaded data, so a new dataset
    only needs DATASET_ITEM_LABEL changed -- no code edits."""
    values = {
        "label": constants.DATASET_ITEM_LABEL,
        "aspects": ", ".join(get_aspects()),
        "low": constants.SEVERITY_MIN,
        "high": constants.SEVERITY_MAX,
    }
    return {
        column: template.format(**values)
        for column, template in constants.COLUMN_DESCRIPTION_TEMPLATES.items()
    }


def get_date_range():
    """First and last review date (ISO strings), used to limit the date
    pickers to dates that have data. None for both if there are no dates."""
    df = load_reviews()
    dates = df["datetime"].dropna()
    if dates.empty:
        return {"min_date": None, "max_date": None}
    return {
        "min_date": dates.min().date().isoformat(),
        "max_date": dates.max().date().isoformat(),
    }


def get_summary(start_date=None, end_date=None, aspect=None):
    df = _filtered(start_date, end_date, aspect)
    if df.empty:
        return {"total_reviews": 0, "avg_rating": 0.0, "negative_pct": 0.0, "high_severity_count": 0}
    return {
        "total_reviews": int(len(df)),
        "avg_rating": round(float(df["Score"].mean()), 2),
        "negative_pct": round(float((df["sentiment"] == "negative").mean() * 100), 1),
        "high_severity_count": int((df["severity"] >= constants.HIGH_SEVERITY_THRESHOLD).sum()),
    }


def get_sentiment_trend(start_date=None, end_date=None, aspect=None):
    df = _filtered(start_date, end_date, aspect)
    if df.empty:
        return {"split": {}, "trend": []}
    split = {key: int(value) for key, value in df["sentiment"].value_counts().to_dict().items()}
    trend_df = (
        df.groupby([df["datetime"].dt.to_period("M").astype(str), "sentiment"])
        .size()
        .reset_index(name="count")
    )
    trend_df.columns = ["month", "sentiment", "count"]
    return {"split": split, "trend": trend_df.to_dict(orient="records")}


def get_aspect_breakdown(start_date=None, end_date=None):
    df = _filtered(start_date, end_date)
    if df.empty:
        return []
    stats = (
        df.groupby("aspect")
        .agg(count=("Id", "count"),
             negative_pct=("sentiment", lambda s: round((s == "negative").mean() * 100, 1)))
        .reset_index()
        .sort_values("count", ascending=False)
    )
    return stats.to_dict(orient="records")


def get_top_products(start_date=None, end_date=None, limit=constants.DASHBOARD_TOP_PRODUCTS_LIMIT):
    df = _filtered(start_date, end_date)
    if df.empty:
        return []
    top = (
        df.groupby("ProductName")
        .agg(reviews=("Id", "count"), avg_score=("Score", "mean"))
        .reset_index()
        .sort_values("reviews", ascending=False)
        .head(limit)
    )
    top["avg_score"] = top["avg_score"].round(2)
    return top.to_dict(orient="records")


def get_flagged_reviews_view(min_severity=constants.DEFAULT_MIN_SEVERITY, start_date=None,
                             end_date=None, aspect=None, search=None):
    df = _filtered(start_date, end_date, aspect)
    df = df[df["severity"] >= min_severity]
    if search:
        mask = (
            df["ProductName"].str.contains(search, case=False, na=False)
            | df["Summary"].str.contains(search, case=False, na=False)
            | df["Text"].str.contains(search, case=False, na=False)
        )
        df = df[mask]
    df = df.sort_values(["severity", "datetime"], ascending=[False, False])
    result = df[["ProductName", "severity", "sentiment", "aspect", "datetime", "Summary"]].copy()
    result["datetime"] = result["datetime"].dt.strftime("%Y-%m-%d")
    result.columns = ["product", "severity", "sentiment", "aspect", "date", "summary"]
    return result.to_dict(orient="records")


async def generate_report_now():
    """Manual "generate report" trigger for the dashboard button. Runs the
    same code the scheduler/CLI script use, off the event loop thread
    since it does blocking pandas work, and returns the freshly written
    report so the caller doesn't need a second round trip to read the file.

    Raises DataNotFoundError if there were no reviews in the report window
    (nothing gets written in that case, same as the scheduler).
    """
    result = await asyncio.to_thread(run_report_once)
    if result["status"] == "empty":
        raise DataNotFoundError(
            f"No reviews found between {result['start_date']} and {result['end_date']}; "
            "nothing was generated."
        )
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "start_date": result["start_date"],
        "end_date": result["end_date"],
        "total_reviews": result["total_reviews"],
        "report_markdown": result["markdown"],
    }


def get_usage_summary(days=constants.USAGE_CHART_DAYS):
    """Model usage for the dashboard's Usage tab: total calls, tokens,
    average latency, estimated cost (if configured), and a per-day series."""
    return summarize_usage(days=days)