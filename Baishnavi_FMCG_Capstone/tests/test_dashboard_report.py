"""Tests for the dashboard_service pieces the other test file does not
reach: the manual report trigger and an empty date range.
"""

import asyncio

import pandas as pd
import pytest

from src.exceptions import DataNotFoundError
from src.services import dashboard_service


class TestGenerateReportNow:
    def test_empty_window_is_reported_as_not_found(self, monkeypatch):
        monkeypatch.setattr(dashboard_service, "run_report_once", lambda: {
            "status": "empty", "start_date": "2013-01-01", "end_date": "2013-01-07",
        })
        with pytest.raises(DataNotFoundError, match="2013-01-01"):
            asyncio.run(dashboard_service.generate_report_now())

    def test_successful_run_returns_the_report_payload(self, monkeypatch):
        monkeypatch.setattr(dashboard_service, "run_report_once", lambda: {
            "status": "ok", "markdown": "# Weekly report", "total_reviews": 12,
            "start_date": "2013-01-01", "end_date": "2013-01-07",
        })
        result = asyncio.run(dashboard_service.generate_report_now())
        assert result["report_markdown"] == "# Weekly report"
        assert result["total_reviews"] == 12
        assert result["start_date"] == "2013-01-01" and result["end_date"] == "2013-01-07"
        assert result["generated_at"]  # an ISO timestamp


class TestEmptyDateRange:
    def test_no_dates_gives_none_for_both_bounds(self, monkeypatch):
        frame = pd.DataFrame({"datetime": pd.to_datetime([None, None])})
        monkeypatch.setattr(dashboard_service, "load_reviews", lambda: frame)
        assert dashboard_service.get_date_range() == {"min_date": None, "max_date": None}
