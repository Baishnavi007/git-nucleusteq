"""Tests for the audit log helper (src/utils/llm_logger.py)."""

from src.utils import llm_logger


def test_log_call_appends_a_json_line(tmp_path, monkeypatch):
    log_path = tmp_path / "agent_calls.jsonl"
    monkeypatch.setattr(llm_logger.constants, "AGENT_CALLS_LOG_PATH", log_path)

    llm_logger.log_call(
        framework="test", query="how many negative reviews last week?",
        tool_calls=["flagged_reviews"], prompt_tokens=120, completion_tokens=40,
        latency_ms=250.0, response_preview="There were 3 negative reviews.",
    )

    entries = llm_logger.read_all_calls()
    assert len(entries) == 1
    assert entries[0]["tool_calls"] == ["flagged_reviews"]
    assert entries[0]["total_tokens"] == 160


def test_timer_measures_elapsed_time():
    import time
    with llm_logger.Timer() as timer:
        time.sleep(0.01)
    assert timer.elapsed_ms >= 5


def test_summarize_usage_totals_tokens(tmp_path, monkeypatch):
    from src.utils import llm_logger

    log_path = tmp_path / "agent_calls.jsonl"
    monkeypatch.setattr(llm_logger.constants, "AGENT_CALLS_LOG_PATH", log_path)

    for prompt_tokens, completion_tokens in [(100, 20), (200, 30)]:
        llm_logger.log_call(
            framework="test", query="q", tool_calls=[],
            prompt_tokens=prompt_tokens, completion_tokens=completion_tokens,
            latency_ms=100.0, response_preview="a",
        )

    summary = llm_logger.summarize_usage(days=30)
    assert summary["total_calls"] == 2
    assert summary["total_prompt_tokens"] == 300
    assert summary["total_completion_tokens"] == 50
    assert summary["total_tokens"] == 350
