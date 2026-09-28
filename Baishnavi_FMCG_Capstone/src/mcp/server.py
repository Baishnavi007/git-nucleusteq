"""
server.py
====================
Exposes the four review-intelligence tools over MCP, so the agent calls
them over the real MCP protocol. Started by the agent as a subprocess:

    python -m src.mcp.server        (run from the project root)

Requires mcp<2 (pip install "mcp<2") for the FastMCP import below; mcp 2.x
renamed FastMCP.

stdout is the MCP protocol channel: never print() here. Use the logger
(it writes to stderr and to logs/mcp_server.log).
"""

import os
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("LOG_FILE_NAME", "mcp_server.log")

import functools

from mcp.server.fastmcp import FastMCP

from src.config import constants
from src.exceptions import AppError
from src.mcp.tools.flagged_reviews import flagged_reviews as _flagged_reviews
from src.mcp.tools.search_reviews import search_reviews as _search_reviews
from src.mcp.tools.sentiment_trends import sentiment_trends as _sentiment_trends
from src.mcp.tools.summary_report import summary_report as _summary_report
from src.utils.logger import get_logger

logger = get_logger(__name__)

mcp = FastMCP(constants.MCP_SERVER_NAME)


def safe_tool(fn):
    """Catches any exception raised inside a tool and returns it as an error
    entry instead of letting it cross the MCP boundary. A raw exception there
    is mangled by a known langchain-mcp-adapters bug (UnboundLocalError:
    'call_tool_result') that hides the real error. Full details go to the log."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except AppError as error:
            logger.warning("Tool %s rejected the request: %s", fn.__name__, error.message)
            return [{"error": error.message, "error_code": error.error_code}]
        except Exception as error:
            logger.exception("Tool %s failed | args=%s kwargs=%s", fn.__name__, args, kwargs)
            return [{"error": f"{fn.__name__} failed: {type(error).__name__}: {error}"}]
    return wrapper


# NOTE: the type hints on the four tool functions below are intentional and
# must stay. FastMCP reads them to build the argument schema the LLM sees;
# without them the model would get untyped arguments and call the tools worse.

@mcp.tool()
@safe_tool
def sentiment_trends(aspect: str | None = None, start_date: str | None = None,
                     end_date: str | None = None, granularity: str = "week") -> dict:
    """Get sentiment counts over time, optionally scoped to one review aspect."""
    return _sentiment_trends(aspect, start_date, end_date, granularity)


@mcp.tool()
@safe_tool
def flagged_reviews(min_severity: int = constants.DEFAULT_MIN_SEVERITY, start_date: str | None = None,
                    end_date: str | None = None, aspect: str | None = None,
                    product_id: str | None = None, product_name: str | None = None,
                    limit: int = constants.DEFAULT_FLAG_LIMIT) -> list[dict]:
    """Get high-severity reviews for manual escalation, most severe first.
    Use product_name for a case-insensitive partial name match (e.g.
    "kitten formula"), or product_id for an exact match on Amazon's
    product code. If product_name matches multiple different products,
    the result includes a warning entry rather than silently combining
    them."""
    return _flagged_reviews(min_severity, start_date, end_date, aspect,
                            product_id, product_name, limit)


@mcp.tool()
@safe_tool
def summary_report(start_date: str | None = None, end_date: str | None = None,
                   product_id: str | None = None, product_name: str | None = None) -> dict:
    """Generate a brand-health summary combining trends and flagged reviews.
    Use product_name for a partial case-insensitive name match, or
    product_id for an exact match, to scope the summary to one product."""
    return _summary_report(start_date, end_date, product_id, product_name)


@mcp.tool()
@safe_tool
def search_reviews(query: str, aspect: str | None = None, sentiment: str | None = None,
                   min_severity: int | None = None, product_id: str | None = None,
                   product_name: str | None = None, start_date: str | None = None,
                   end_date: str | None = None, n_results: int = constants.SEARCH_DEFAULT_RESULTS) -> list[dict]:
    """Semantic search over review text for fuzzy, meaning-based queries
    that don't map to a fixed field -- e.g. "weird smell", "package
    arrived leaking", "tastes different than before". Prefer this over
    the other three tools when the user's question describes a theme or
    symptom rather than an exact aspect/severity/date/product filter, or
    when an aspect/sentiment/severity filter alone returned nothing
    useful and the user's actual complaint is more specific than that.
    Do NOT use this for aggregations or "how many/all reviews" questions
    -- it returns approximate top matches, not a complete set; use
    sentiment_trends/flagged_reviews/summary_report for those instead."""
    return _search_reviews(query, aspect, sentiment, min_severity, product_id,
                           product_name, start_date, end_date, n_results)


def warm_up():
    """Loads the embedding model and vector store before the first client
    request, so the first search is not slow."""
    try:
        _search_reviews(query="warmup", n_results=1)
        logger.info("Embedding model and vector store warmed up. Server ready.")
    except Exception:
        logger.exception("Warm-up failed. Search tool will report an error until this is fixed.")


if __name__ == "__main__":
    logger.info("MCP server starting")
    warm_up()
    # Let FastMCP initialise the stdio channel only after warm-up is done.
    mcp.run()
