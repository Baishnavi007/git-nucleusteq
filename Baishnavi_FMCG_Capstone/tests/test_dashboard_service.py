"""Tests for src/services/dashboard_service.py, against the same synthetic
fixture used for the tool tests, so the dashboard and the agent are checked
against one consistent picture of the data."""

from src.config import constants
from src.services import dashboard_service


class TestGetAspects:
    def test_returns_sorted_distinct_aspects(self, synthetic_reviews_env):
        assert dashboard_service.get_aspects() == ["other", "packaging", "price", "taste"]


class TestGetDateRange:
    def test_returns_the_dataset_bounds(self, synthetic_reviews_env):
        bounds = dashboard_service.get_date_range()
        assert bounds == {"min_date": "2013-01-01", "max_date": "2013-01-05"}


class TestGetSummary:
    def test_totals_match_the_fixture(self, synthetic_reviews_env):
        summary = dashboard_service.get_summary()
        assert summary["total_reviews"] == 5
        assert summary["high_severity_count"] == 2  # severities 3 and 5

    def test_empty_filter_returns_zeroed_summary(self, synthetic_reviews_env):
        summary = dashboard_service.get_summary(start_date="1999-01-01", end_date="1999-01-02")
        assert summary == {
            "total_reviews": 0, "avg_rating": 0.0,
            "negative_pct": 0.0, "high_severity_count": 0,
        }

    def test_aspect_filter_narrows_the_count(self, synthetic_reviews_env):
        summary = dashboard_service.get_summary(aspect="taste")
        assert summary["total_reviews"] == 1


class TestGetSentimentTrend:
    def test_split_counts_every_sentiment(self, synthetic_reviews_env):
        trend = dashboard_service.get_sentiment_trend()
        assert trend["split"]["negative"] == 3
        assert trend["split"]["positive"] == 2

    def test_empty_filter_returns_empty_shape(self, synthetic_reviews_env):
        trend = dashboard_service.get_sentiment_trend(start_date="1999-01-01", end_date="1999-01-02")
        assert trend == {"split": {}, "trend": []}


class TestGetAspectBreakdown:
    def test_one_row_per_aspect(self, synthetic_reviews_env):
        rows = dashboard_service.get_aspect_breakdown()
        aspects = {row["aspect"] for row in rows}
        assert aspects == {"taste", "other", "packaging", "price"}

    def test_empty_filter_returns_empty_list(self, synthetic_reviews_env):
        assert dashboard_service.get_aspect_breakdown(start_date="1999-01-01", end_date="1999-01-02") == []


class TestGetTopProducts:
    def test_respects_the_limit(self, synthetic_reviews_env):
        rows = dashboard_service.get_top_products(limit=1)
        assert len(rows) == 1

    def test_most_reviewed_product_is_first(self, synthetic_reviews_env):
        rows = dashboard_service.get_top_products()
        assert rows[0]["ProductName"] in ("Chicken Formula", "Beef Formula")
        assert rows[0]["reviews"] == 2


class TestGetFlaggedReviewsView:
    def test_only_high_severity_rows_come_back(self, synthetic_reviews_env):
        rows = dashboard_service.get_flagged_reviews_view(min_severity=3)
        assert len(rows) == 2
        assert all(row["severity"] >= 3 for row in rows)

    def test_sorted_most_severe_first(self, synthetic_reviews_env):
        rows = dashboard_service.get_flagged_reviews_view(min_severity=0)
        severities = [row["severity"] for row in rows]
        assert severities == sorted(severities, reverse=True)

    def test_search_filters_by_keyword(self, synthetic_reviews_env):
        rows = dashboard_service.get_flagged_reviews_view(min_severity=0, search="mold")
        assert len(rows) == 1
        assert rows[0]["product"] == "Salmon Formula"

    def test_search_with_no_match_returns_empty(self, synthetic_reviews_env):
        assert dashboard_service.get_flagged_reviews_view(min_severity=0, search="nonexistent-word") == []


class TestGetUsageSummary:
    def test_delegates_to_llm_logger(self, tmp_path, monkeypatch, synthetic_reviews_env):
        from src.utils import llm_logger
        monkeypatch.setattr(llm_logger.constants, "AGENT_CALLS_LOG_PATH", tmp_path / "agent_calls.jsonl")
        llm_logger.log_call(framework="t", query="q", tool_calls=[], prompt_tokens=10,
                            completion_tokens=5, latency_ms=50.0, response_preview="a")
        usage = dashboard_service.get_usage_summary(days=30)
        assert usage["total_calls"] == 1
        assert usage["total_tokens"] == 15