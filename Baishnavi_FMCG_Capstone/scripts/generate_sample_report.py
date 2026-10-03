"""
generate_sample_report.py
==========================
Writes one summary_report() call to disk as a readable Markdown file --
the "generated sample weekly brand-health report" deliverable. Uses the
most recent REPORT_WINDOW_DAYS of data in the dataset (not the real
calendar week, since the review data is historical).

This is the same report-generation code the in-process scheduler
(src/services/report_scheduler.py) uses when REPORT_SCHEDULE_ENABLED=true
-- run this script by hand, or from your own cron/Task Scheduler, as an
alternative to turning that scheduler on.

Run from the project root:
    python -m scripts.generate_sample_report
"""

import sys

from src.exceptions import AppError
from src.services.report_scheduler import run_report_once
from src.utils.logger import get_logger

logger = get_logger(__name__)


if __name__ == "__main__":
    try:
        run_report_once()
    except AppError as error:
        logger.error("%s", error.message)
        sys.exit(1)
    except Exception:
        logger.exception("Report generation failed")
        sys.exit(1)
