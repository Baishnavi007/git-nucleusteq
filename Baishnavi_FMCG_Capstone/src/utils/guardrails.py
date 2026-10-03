"""
guardrails.py
====================
Defense-in-depth layer for prompt-injection attempts embedded in review
text. This does NOT replace the agent's system-prompt instruction (that is
still the primary defense) -- it is a second, code-level check: scan review
text before it is handed to the LLM, and log every detection to an audit
trail whether or not the LLM would have resisted.

Works on whatever field names the calling tool actually returns (pass
`text_fields`) rather than assuming "summary"/"text" -- passing the wrong
field names used to mean nothing was ever scanned.
"""

import json
import re
import unicodedata
from datetime import datetime, timezone

from src.config import constants
from src.utils.logger import get_logger

logger = get_logger(__name__)

_COMPILED = [re.compile(pattern, re.IGNORECASE) for pattern in constants.SUSPICIOUS_PATTERNS]
_ZERO_WIDTH_RE = re.compile("[" + constants.ZERO_WIDTH_CHARS + "]")


def _normalize(text):
    """Strips zero-width characters and normalizes unicode, so an attacker
    can't hide a pattern by inserting invisible characters or lookalike
    glyphs between its letters."""
    text = unicodedata.normalize("NFKC", text)
    return _ZERO_WIDTH_RE.sub("", text)


def scan_for_injection(text):
    """Returns the suspicious patterns matched in this text. Empty list = clean."""
    if not text:
        return []
    text = _normalize(text)
    return [pattern.pattern for pattern in _COMPILED if pattern.search(text)]


def log_injection_attempt(review_id, product_id, matched_patterns, text_preview, context_query=""):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "review_id": review_id,
        "product_id": product_id,
        "matched_patterns": matched_patterns,
        "text_preview": (text_preview or "")[:constants.INJECTION_PREVIEW_CHARS],
        "context_query": context_query,
    }
    try:
        constants.INJECTION_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(constants.INJECTION_LOG_PATH, "a", encoding="utf-8") as file:
            file.write(json.dumps(entry) + "\n")
    except OSError:
        logger.exception("Could not write to %s", constants.INJECTION_LOG_PATH)
    logger.warning("Possible prompt injection in review %s (product %s)", review_id, product_id)


def flag_suspicious_reviews(reviews, text_fields, context_query=""):
    """Scans each review dict's `text_fields` for injection-pattern matches.
    Reviews are NOT altered or removed -- the LLM must still see the real
    text and reason about it as data. Matches are logged to the audit trail
    and a 'content_warning' field is added to the flagged item.

    Args:
        reviews: list of review dicts. Non-review placeholder dicts (no
            'review_id' key, e.g. {"message": ...} or {"warning": ...}) are
            passed through unscanned.
        text_fields: names of the keys in each review dict that hold
            free text to scan, e.g. ("summary", "text") or ("review_text",).
            Passing the field names that don't exist in `reviews` is a bug
            in the caller, not a silent no-op -- callers must match their
            own return shape.
    """
    for review in reviews:
        if not isinstance(review, dict) or "review_id" not in review:
            continue

        combined_text = " ".join(str(review.get(field, "")) for field in text_fields)
        matches = scan_for_injection(combined_text)

        if matches:
            log_injection_attempt(
                review_id=review.get("review_id"),
                product_id=review.get("product_id"),
                matched_patterns=matches,
                text_preview=combined_text,
                context_query=context_query,
            )
            review["content_warning"] = constants.INJECTION_CONTENT_WARNING

    return reviews


def read_all_injection_attempts():
    """Reads back the full audit log, for the doc/eval write-up."""
    if not constants.INJECTION_LOG_PATH.exists():
        return []
    with open(constants.INJECTION_LOG_PATH, "r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]
