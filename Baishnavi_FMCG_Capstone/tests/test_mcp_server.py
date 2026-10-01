"""Tests for src/mcp/server.py: the safe_tool wrapper, the argument
forwarding of the four tool functions, and warm_up. The real tools are
replaced with fakes, so no data, embedding model or MCP transport is used.
"""

import pytest

from src.exceptions import InvalidInputError
from src.mcp import server


def plain(tool):
    """FastMCP may hand back the function itself or a Tool object with .fn."""
    return getattr(tool, "fn", tool)


class TestSafeTool:
    def test_passes_a_normal_result_through(self):
        @server.safe_tool
        def my_tool(x):
            return [x * 2]

        assert my_tool(4) == [8]

    def test_keeps_the_function_name(self):
        @server.safe_tool
        def my_tool():
            return []

        assert my_tool.__name__ == "my_tool"

    def test_app_errors_become_an_error_entry_with_a_code(self):
        @server.safe_tool
        def my_tool():
            raise InvalidInputError("aspect is wrong")

        assert my_tool() == [{"error": "aspect is wrong", "error_code": "INVALID_INPUT"}]

    def test_unexpected_errors_become_an_error_entry(self):
        @server.safe_tool
        def my_tool():
            raise ValueError("boom")

        assert my_tool() == [{"error": "my_tool failed: ValueError: boom"}]


class TestToolForwarding:
    def test_sentiment_trends_forwards_its_arguments(self, monkeypatch):
        monkeypatch.setattr(server, "_sentiment_trends", lambda *args: ("trend", args))
        result = plain(server.sentiment_trends)("taste", "2013-01-01", "2013-02-01", "month")
        assert result == ("trend", ("taste", "2013-01-01", "2013-02-01", "month"))

    def test_flagged_reviews_forwards_its_arguments(self, monkeypatch):
        monkeypatch.setattr(server, "_flagged_reviews", lambda *args: ("flagged", args))
        result = plain(server.flagged_reviews)(4, "2013-01-01", "2013-02-01", "price", "P1", "Beef", 7)
        assert result == ("flagged", (4, "2013-01-01", "2013-02-01", "price", "P1", "Beef", 7))

    def test_summary_report_forwards_its_arguments(self, monkeypatch):
        monkeypatch.setattr(server, "_summary_report", lambda *args: ("report", args))
        result = plain(server.summary_report)("2013-01-01", "2013-02-01", "P1", "Beef")
        assert result == ("report", ("2013-01-01", "2013-02-01", "P1", "Beef"))

    def test_search_reviews_forwards_its_arguments(self, monkeypatch):
        monkeypatch.setattr(server, "_search_reviews", lambda *args: ("found", args))
        result = plain(server.search_reviews)(
            "weird smell", "taste", "negative", 2, "P1", "Beef", "2013-01-01", "2013-02-01", 5,
        )
        assert result == ("found", ("weird smell", "taste", "negative", 2, "P1", "Beef",
                                    "2013-01-01", "2013-02-01", 5))

    def test_a_failing_tool_is_reported_not_raised(self, monkeypatch):
        def rejecting(*_args):
            raise InvalidInputError("min_severity must be between 0 and 5.")

        monkeypatch.setattr(server, "_flagged_reviews", rejecting)
        result = plain(server.flagged_reviews)(9)
        assert result[0]["error_code"] == "INVALID_INPUT"


class TestWarmUp:
    def test_runs_one_tiny_search(self, monkeypatch):
        seen = {}
        monkeypatch.setattr(server, "_search_reviews", lambda **kwargs: seen.update(kwargs))
        server.warm_up()
        assert seen == {"query": "warmup", "n_results": 1}

    def test_a_failed_warm_up_does_not_stop_the_server(self, monkeypatch):
        def broken(**_kwargs):
            raise RuntimeError("model missing")

        monkeypatch.setattr(server, "_search_reviews", broken)
        server.warm_up()  # should only log
