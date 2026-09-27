"""
logger.py
====================
One place that configures logging for the whole project.

    from src.utils.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Loaded %s reviews", count)

Two rules that matter here:
  * Console output goes to STDERR, never stdout. When the MCP server runs
    as a subprocess, stdout is the protocol channel and anything written
    there corrupts it.
  * Each process writes its own file (chosen by LOG_FILE_NAME in
    constants.py) plus a matching *_errors.log that only holds ERROR and
    above, so the important lines are easy to find.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler

from src.config import constants

_configured = False


def setup_logging():
    """Configures the project logger once per process. Safe to call twice."""
    global _configured
    if _configured:
        return

    root = logging.getLogger(constants.LOGGER_ROOT_NAME)
    root.setLevel(constants.LOG_LEVEL)
    root.propagate = False
    formatter = logging.Formatter(constants.LOG_FORMAT, constants.LOG_DATE_FORMAT)

    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(formatter)
    root.addHandler(console)

    try:
        constants.LOG_DIR.mkdir(parents=True, exist_ok=True)
        stem = constants.LOG_FILE_NAME.rsplit(".", 1)[0]

        app_file = RotatingFileHandler(
            constants.LOG_DIR / constants.LOG_FILE_NAME,
            maxBytes=constants.LOG_MAX_BYTES,
            backupCount=constants.LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        app_file.setFormatter(formatter)
        root.addHandler(app_file)

        error_file = RotatingFileHandler(
            constants.LOG_DIR / f"{stem}_errors.log",
            maxBytes=constants.LOG_MAX_BYTES,
            backupCount=constants.LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        error_file.setLevel(logging.ERROR)
        error_file.setFormatter(formatter)
        root.addHandler(error_file)
    except OSError as error:
        root.warning("File logging disabled, could not open log files: %s", error)

    _configured = True


def get_logger(name):
    setup_logging()
    return logging.getLogger(f"{constants.LOGGER_ROOT_NAME}.{name}")
