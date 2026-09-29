"""Tests for src/services/report_scheduler.py: the pure Markdown renderer,
the history logger, and run_report_once() with summary_report() and
get_dataset_today() replaced by fakes -- no dataset, no Groq key needed.

The always-on background loop (_scheduler_loop / _run_and_log) sleeps for
real minutes/hours between iterations and is exercised by hand when the
scheduler is enabled in .env, rather than here.
"""

import asyncio
import json
from datetime import date

import pytest

from src.services import report_scheduler


SAMPLE_REPORT = {
    "total_reviews": 12,
    "overall_sentiment": {"negative": 8, "positive": 4},
    "aspect_breakdown": {"packaging": {"count": 5, "negative_pct": 80.0}},
    "sentiment_trend": [
        {"period": "2013-01-01", "negative_pct": 50.0, "negative_pct_change": None},
        {"period": "2013-01-08", "negative_pct": 66.7, "negative_pct_change": 16.7},
    ],
    "top_flagged_reviews": [
        {"review_id": 5, "severity": 5, "product_name": "Salmon Formula", "summary": "Contamination"},
        {"message": "No reviews found matching these filters."},
    ],
}


class TestRenderMarkdown:
    def test_includes_the_headline_numbers(self):
        markdown = report_scheduler._render_markdown(SAMPLE_REPORT, date(2013, 1, 1), date(2013, 1, 8))
        assert "Total reviews: **12**" in markdown
        assert "- negative: 8" in markdown

    def test_includes_the_aspect_breakdown(self):
        markdown = report_scheduler._render_markdown(SAMPLE_REPORT, date(2013, 1, 1), date(2013, 1, 8))
        assert "**packaging**: 5 reviews, 80.0% negative" in markdown

    def test_shows_the_change_when_present_and_omits_it_when_none(self):
        markdown = report_scheduler._render_markdown(SAMPLE_REPORT, date(2013, 1, 1), date(2013, 1, 8))
        assert "+16.7 pts vs. prior period" in markdown
        # the first period has no prior period, so no "pts vs." for that line
        first_period_line = [line for line in markdown.splitlines() if "2013-01-01:" in line][0]
        assert "pts vs." not in first_period_line

    def test_lists_only_real_flagged_reviews(self):
        markdown = report_scheduler._render_markdown(SAMPLE_REPORT, date(2013, 1, 1), date(2013, 1, 8))
        assert "#5, severity 5" in markdown
        assert "No reviews found" not in markdown  # placeholder entries are skipped

    def test_handles_no_trend_and_no_flags(self):
        minimal = {
            "total_reviews": 0, "overall_sentiment": {}, "aspect_breakdown": {},
            "sentiment_trend": [], "top_flagged_reviews": [],
        }
        markdown = report_scheduler._render_markdown(minimal, date(2013, 1, 1), date(2013, 1, 1))
        assert "## Trend" not in markdown  # empty trend list is skipped entirely


class TestLogRun:
    def test_appends_a_json_line(self, tmp_path, monkeypatch):
        history_path = tmp_path / "report_history.jsonl"
        monkeypatch.setattr(report_scheduler.constants, "REPORT_HISTORY_PATH", history_path)
        monkeypatch.setattr(report_scheduler.constants, "DOCS_DIR", tmp_path)

        report_scheduler._log_run("ok", "12 reviews")
        report_scheduler._log_run("empty", "no reviews in range")

        lines = history_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        first = json.loads(lines[0])
        assert first["status"] == "ok" and first["detail"] == "12 reviews"


class TestRunReportOnce:
    def test_writes_the_report_file_on_success(self, tmp_path, monkeypatch):
        monkeypatch.setattr(report_scheduler, "get_dataset_today", lambda: date(2013, 1, 8))
        monkeypatch.setattr(report_scheduler, "summary_report", lambda start_date, end_date: SAMPLE_REPORT)
        report_path = tmp_path / "sample_weekly_report.md"
        history_path = tmp_path / "report_history.jsonl"
        monkeypatch.setattr(report_scheduler.constants, "SAMPLE_REPORT_PATH", report_path)
        monkeypatch.setattr(report_scheduler.constants, "REPORT_HISTORY_PATH", history_path)
        monkeypatch.setattr(report_scheduler.constants, "DOCS_DIR", tmp_path)

        report_scheduler.run_report_once()

        assert report_path.exists()
        assert "Total reviews: **12**" in report_path.read_text(encoding="utf-8")
        entry = json.loads(history_path.read_text(encoding="utf-8").splitlines()[-1])
        assert entry["status"] == "ok"

    def test_empty_range_logs_and_writes_nothing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(report_scheduler, "get_dataset_today", lambda: date(2013, 1, 8))
        monkeypatch.setattr(
            report_scheduler, "summary_report",
            lambda start_date, end_date: {"message": "No reviews found matching these filters."},
        )
        report_path = tmp_path / "sample_weekly_report.md"
        history_path = tmp_path / "report_history.jsonl"
        monkeypatch.setattr(report_scheduler.constants, "SAMPLE_REPORT_PATH", report_path)
        monkeypatch.setattr(report_scheduler.constants, "REPORT_HISTORY_PATH", history_path)
        monkeypatch.setattr(report_scheduler.constants, "DOCS_DIR", tmp_path)

        report_scheduler.run_report_once()

        assert not report_path.exists()
        entry = json.loads(history_path.read_text(encoding="utf-8").splitlines()[-1])
        assert entry["status"] == "empty"


class TestStartStopScheduler:
    def test_disabled_returns_none_and_starts_nothing(self, monkeypatch):
        monkeypatch.setattr(report_scheduler.constants, "REPORT_SCHEDULE_ENABLED", False)
        report_scheduler._task = None
        assert report_scheduler.start_scheduler() is None

    def test_stop_with_no_running_task_is_a_no_op(self):
        report_scheduler._task = None
        asyncio.run(report_scheduler.stop_scheduler())  # should not raise