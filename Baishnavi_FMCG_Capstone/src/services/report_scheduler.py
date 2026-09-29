"""
report_scheduler.py
====================
Runs scripts/generate_sample_report's report generation on a repeating
interval, as a background asyncio task inside the same process as the API
-- no extra dependency (APScheduler, Celery, cron) required.

Off by default. Turn it on with REPORT_SCHEDULE_ENABLED=true in .env; the
interval is REPORT_SCHEDULE_INTERVAL_SECONDS (default: 7 days). If you'd
rather trigger reports from your OS's own scheduler (cron, Task Scheduler,
a CI job) instead, leave this off and run
`python -m scripts.generate_sample_report` from there -- both write the
same file and neither depends on the other.

Each run's outcome (including failures) is appended to
docs/report_history.jsonl so there's a record of whether/when reports
actually ran, separate from the report content itself.
"""

import asyncio
import json
from datetime import datetime, timedelta, timezone

from src.config import constants
from src.exceptions import AppError
from src.mcp.tools.summary_report import summary_report
from src.repositories.data_access import get_dataset_today
from src.utils.logger import get_logger

logger = get_logger(__name__)

_task = None


def _render_markdown(report, start_date, end_date):
    lines = [
        f"# Weekly Brand-Health Report: {start_date} to {end_date}",
        "", f"Total reviews: **{report['total_reviews']}**", "",
        "## Overall sentiment", "",
    ]
    for sentiment, count in report["overall_sentiment"].items():
        lines.append(f"- {sentiment}: {count}")

    lines += ["", "## By aspect", ""]
    for aspect, stats in report["aspect_breakdown"].items():
        lines.append(f"- **{aspect}**: {stats['count']} reviews, {stats['negative_pct']}% negative")

    if report.get("sentiment_trend"):
        lines += ["", "## Trend", ""]
        for period in report["sentiment_trend"]:
            change = period.get("negative_pct_change")
            change_text = "" if change is None else f" ({change:+.1f} pts vs. prior period)"
            lines.append(f"- {period['period']}: {period['negative_pct']}% negative{change_text}")

    lines += ["", "## Top flagged reviews", ""]
    for item in report["top_flagged_reviews"]:
        if "message" in item or "warning" in item:
            continue
        lines.append(f"- (#{item['review_id']}, severity {item['severity']}) "
                     f"{item['product_name']}: {item['summary']}")

    return "\n".join(lines) + "\n"


def _log_run(status, detail=""):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "detail": detail,
    }
    try:
        constants.DOCS_DIR.mkdir(parents=True, exist_ok=True)
        with open(constants.REPORT_HISTORY_PATH, "a", encoding="utf-8") as file:
            file.write(json.dumps(entry) + "\n")
    except OSError:
        logger.exception("Could not write to %s", constants.REPORT_HISTORY_PATH)


def run_report_once():
    """Generates one report and writes it to constants.SAMPLE_REPORT_PATH.
    Runs in a thread (see _scheduler_loop) since it does blocking pandas
    work; safe to also call directly/synchronously, e.g. from a script."""
    end_date = get_dataset_today()
    start_date = end_date - timedelta(days=constants.REPORT_WINDOW_DAYS - 1)

    report = summary_report(start_date=start_date.isoformat(), end_date=end_date.isoformat())
    if "message" in report:
        logger.warning("Scheduled report: no reviews in %s to %s (%s)",
                       start_date, end_date, report["message"])
        _log_run("empty", report["message"])
        return

    markdown = _render_markdown(report, start_date, end_date)
    constants.DOCS_DIR.mkdir(parents=True, exist_ok=True)
    constants.SAMPLE_REPORT_PATH.write_text(markdown, encoding="utf-8")
    logger.info("Scheduled report written -> %s", constants.SAMPLE_REPORT_PATH)
    _log_run("ok", f"{report['total_reviews']} reviews, {start_date} to {end_date}")


async def _scheduler_loop():
    if constants.REPORT_SCHEDULE_RUN_ON_STARTUP:
        await _run_and_log()

    while True:
        try:
            await asyncio.sleep(constants.REPORT_SCHEDULE_INTERVAL_SECONDS)
            await _run_and_log()
        except asyncio.CancelledError:
            logger.info("Report scheduler stopped")
            raise


async def _run_and_log():
    try:
        await asyncio.to_thread(run_report_once)
    except AppError as error:
        logger.error("Scheduled report failed: %s", error.message)
        _log_run("error", error.message)
        # A configuration/data problem probably won't fix itself before the
        # next full interval; retry sooner instead of waiting a full cycle.
        await asyncio.sleep(constants.REPORT_SCHEDULE_RETRY_SECONDS)
    except Exception:
        logger.exception("Scheduled report failed unexpectedly")
        _log_run("error", "unexpected failure, see app log")
        await asyncio.sleep(constants.REPORT_SCHEDULE_RETRY_SECONDS)


def start_scheduler():
    """Starts the background task. No-op (returns None) if disabled or
    already running."""
    global _task
    if not constants.REPORT_SCHEDULE_ENABLED:
        logger.info("Report scheduler disabled (REPORT_SCHEDULE_ENABLED=false)")
        return None
    if _task is not None:
        return _task
    logger.info("Report scheduler enabled: every %ss, run_on_startup=%s",
                constants.REPORT_SCHEDULE_INTERVAL_SECONDS, constants.REPORT_SCHEDULE_RUN_ON_STARTUP)
    _task = asyncio.create_task(_scheduler_loop())
    return _task


async def stop_scheduler():
    global _task
    if _task is None:
        return
    _task.cancel()
    try:
        await _task
    except asyncio.CancelledError:
        pass
    _task = None
