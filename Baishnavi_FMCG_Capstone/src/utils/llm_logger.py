"""
llm_logger.py
====================
Audit trail for agent calls: appends one JSON object per call to
logs/agent_calls.jsonl (tokens, latency, tools used, answer preview).
JSONL rather than one big JSON array, so a crash mid-run never corrupts
earlier entries and the file can be tailed live.

    from src.utils.llm_logger import log_call, Timer

    with Timer() as timer:
        result = do_the_llm_call()
    log_call(framework="langgraph", query=question, tool_calls=["flagged_reviews"],
             prompt_tokens=100, completion_tokens=20, latency_ms=timer.elapsed_ms)
"""

import json
import time
from datetime import datetime, timedelta, timezone

from src.config import constants
from src.utils.logger import get_logger

logger = get_logger(__name__)


def log_call(framework, query, tool_calls, prompt_tokens, completion_tokens,
             latency_ms, response_preview=""):
    """Appends one call record to logs/agent_calls.jsonl.

    framework: label for the agent/model that answered.
    query: the user's original question.
    tool_calls: names of the tools the agent used (empty list if none).
    prompt_tokens / completion_tokens: usage reported by the LLM.
    latency_ms: wall-clock time for the call, from Timer().
    response_preview: start of the final answer, cut to a short preview.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "framework": framework,
        "query": query,
        "tool_calls": tool_calls,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
        "latency_ms": round(latency_ms, 1),
        "response_preview": response_preview[:constants.RESPONSE_PREVIEW_CHARS],
    }
    try:
        constants.AGENT_CALLS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(constants.AGENT_CALLS_LOG_PATH, "a", encoding="utf-8") as file:
            file.write(json.dumps(entry) + "\n")
    except OSError:
        # Never let an audit-log problem break a user's answer.
        logger.exception("Could not write to %s", constants.AGENT_CALLS_LOG_PATH)


class Timer:
    """Context manager for wall-clock timing.

        with Timer() as timer:
            do_the_llm_call()
        print(timer.elapsed_ms)
    """

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, *exc_info):
        self.elapsed_ms = (time.perf_counter() - self._start) * 1000


def read_all_calls():
    """Reads back every logged call. Returns [] if no log exists yet."""
    if not constants.AGENT_CALLS_LOG_PATH.exists():
        return []
    with open(constants.AGENT_CALLS_LOG_PATH, "r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def summarize_usage(days=constants.USAGE_CHART_DAYS):
    """Aggregates the call log into totals plus a per-day series, for the
    dashboard's usage view. Cost is included only if COST_PER_1K_* rates
    are configured (both default to 0, meaning "not configured").

    Returns:
        {
          "total_calls": int, "total_prompt_tokens": int,
          "total_completion_tokens": int, "total_tokens": int,
          "avg_latency_ms": float, "estimated_cost_usd": float | None,
          "cost_configured": bool,
          "daily": [{"date": "...", "calls": int, "tokens": int}, ...],
          "recent_calls": [...],  # most recent USAGE_RECENT_CALLS_LIMIT, newest first
        }
    """
    calls = read_all_calls()
    if not calls:
        return {
            "total_calls": 0, "total_prompt_tokens": 0, "total_completion_tokens": 0,
            "total_tokens": 0, "avg_latency_ms": 0.0, "estimated_cost_usd": 0.0,
            "cost_configured": bool(constants.COST_PER_1K_PROMPT_TOKENS or constants.COST_PER_1K_COMPLETION_TOKENS),
            "daily": [], "recent_calls": [],
        }

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    total_prompt = sum(c.get("prompt_tokens", 0) for c in calls)
    total_completion = sum(c.get("completion_tokens", 0) for c in calls)
    total_latency = sum(c.get("latency_ms", 0) for c in calls)

    cost_configured = bool(constants.COST_PER_1K_PROMPT_TOKENS or constants.COST_PER_1K_COMPLETION_TOKENS)
    estimated_cost = (
        total_prompt / 1000 * constants.COST_PER_1K_PROMPT_TOKENS
        + total_completion / 1000 * constants.COST_PER_1K_COMPLETION_TOKENS
    )

    by_day = {}
    for call in calls:
        try:
            timestamp = datetime.fromisoformat(call["timestamp"])
        except (KeyError, ValueError):
            continue
        if timestamp < cutoff:
            continue
        day_key = timestamp.date().isoformat()
        bucket = by_day.setdefault(day_key, {"date": day_key, "calls": 0, "tokens": 0})
        bucket["calls"] += 1
        bucket["tokens"] += call.get("total_tokens", 0)

    daily = [by_day[key] for key in sorted(by_day)]
    recent_calls = list(reversed(calls))[:constants.USAGE_RECENT_CALLS_LIMIT]

    return {
        "total_calls": len(calls),
        "total_prompt_tokens": total_prompt,
        "total_completion_tokens": total_completion,
        "total_tokens": total_prompt + total_completion,
        "avg_latency_ms": round(total_latency / len(calls), 1),
        "estimated_cost_usd": round(estimated_cost, 4),
        "cost_configured": cost_configured,
        "daily": daily,
        "recent_calls": recent_calls,
    }


if __name__ == "__main__":
    with Timer() as timer:
        time.sleep(0.05)
    log_call(
        framework="test",
        query="self-test query",
        tool_calls=["dummy_tool"],
        prompt_tokens=100,
        completion_tokens=20,
        latency_ms=timer.elapsed_ms,
        response_preview="this is a self-test log entry",
    )
    calls = read_all_calls()
    logger.info("Log file has %s entries. Last entry: %s", len(calls), json.dumps(calls[-1]))
