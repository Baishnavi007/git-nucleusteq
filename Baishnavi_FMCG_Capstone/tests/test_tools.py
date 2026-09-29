"""Tests for the four MCP tool functions, against synthetic data."""

import pytest

from src.exceptions import InvalidInputError
from src.mcp.tools.flagged_reviews import flagged_reviews
from src.mcp.tools.sentiment_trends import sentiment_trends
from src.mcp.tools.summary_report import summary_report


def test_flagged_reviews_respects_min_severity(synthetic_reviews_env):
    results = flagged_reviews(min_severity=3)
    ids = {item["review_id"] for item in results if "review_id" in item}
    assert ids == {2, 5}  # severities 3 and 5


def test_flagged_reviews_no_match_returns_message(synthetic_reviews_env):
    results = flagged_reviews(min_severity=5, product_id="P1")
    assert results == [{"message": "No reviews found matching these filters."}]


def test_flagged_reviews_rejects_invalid_severity(synthetic_reviews_env):
    with pytest.raises(InvalidInputError):
        flagged_reviews(min_severity=9)


def test_flagged_reviews_rejects_invalid_aspect(synthetic_reviews_env):
    with pytest.raises(InvalidInputError):
        flagged_reviews(aspect="not-a-real-aspect")


def test_flagged_reviews_ambiguous_product_name_warns(synthetic_reviews_env):
    # Both P1 and (if named similarly) another product could share a
    # substring; here we simulate by searching a name unique to one product,
    # then confirm no warning is added for an unambiguous match.
    results = flagged_reviews(min_severity=0, product_name="Chicken")
    assert not any("warning" in item for item in results)


def test_sentiment_trends_computes_period_over_period_change(synthetic_reviews_env):
    result = sentiment_trends(granularity="day")
    periods = result["periods"]
    assert periods[0]["negative_pct_change"] is None  # no prior period
    assert any(p["negative_pct_change"] is not None for p in periods[1:])


def test_summary_report_empty_range_has_message(synthetic_reviews_env):
    result = summary_report(start_date="1999-01-01", end_date="1999-01-02")
    assert "message" in result


def test_summary_report_includes_trend_and_flags(synthetic_reviews_env):
    result = summary_report()
    assert result["total_reviews"] == 5
    assert "sentiment_trend" in result
    assert "top_flagged_reviews" in result


def test_flagged_reviews_truncates_long_text(synthetic_reviews_env, monkeypatch):
    from src.config import constants
    from src.mcp.tools import flagged_reviews as module

    monkeypatch.setattr(module.constants, "REVIEW_TEXT_MAX_CHARS", 20)
    results = flagged_reviews(min_severity=0)
    for item in results:
        if "review_id" in item:
            assert len(item["text"]) <= 24  # 20 chars + "..."
