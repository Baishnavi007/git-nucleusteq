"""
scrub_pii.py
============
Removes reviewer identity data from labeled reviews BEFORE they are
embedded into the vector store. Works on whatever rows are labeled so far.

What gets scrubbed:
  - ProfileName, CustomerEmail, CustomerPhone: masked with a fixed token
    (constants.PII_MASK_TOKEN), NOT dropped, so the schema stays consistent
    and it is auditable that the field existed and was deliberately redacted.
  - Text / Summary: leftover HTML is stripped and email / phone-shaped
    strings are redacted.
  - UserId is Amazon's own opaque ID: left as-is for joining/deduping and
    never shown to end users. It is the only per-customer identifier kept.
  - ProductName / ProductId identify the product, not the person: untouched.

Run from the project root:
    python -m src.rag.scrub_pii

Output:
  - data/processed/scrubbed_reviews.csv   (embed THIS file, never the raw one)
  - docs/pii_policy.md                    (the "how reviewer identity data
                                           is handled" deliverable)
"""

import os
os.environ.setdefault("LOG_FILE_NAME", "pipeline.log")

import html
import re
import sys

import pandas as pd

from src.config import constants
from src.exceptions import AppError, DataNotFoundError
from src.utils.logger import get_logger

logger = get_logger(__name__)

EMAIL_RE = re.compile(constants.EMAIL_PATTERN)
PHONE_RE = re.compile(constants.PHONE_PATTERN)
HTML_TAG_RE = re.compile(constants.HTML_TAG_PATTERN)
WHITESPACE_RE = re.compile(r"\s+")


def clean_html(text):
    """Strips leftover HTML markup and collapses extra whitespace so
    retrieved chunks read as clean prose."""
    if pd.isna(text):
        return text
    text = HTML_TAG_RE.sub(" ", text)
    text = html.unescape(text)  # &amp; -> &, &#39; -> ', etc.
    return WHITESPACE_RE.sub(" ", text).strip()


def redact_contact_info(text):
    if pd.isna(text):
        return text
    text = EMAIL_RE.sub(constants.EMAIL_REDACTION_TEXT, text)
    return PHONE_RE.sub(constants.PHONE_REDACTION_TEXT, text)


def mask_value(value):
    """Replaces a PII value with the mask token. Missing values pass through
    unchanged: masking a NaN would fabricate data that was not there."""
    if pd.isna(value):
        return value
    return constants.PII_MASK_TOKEN


def build_policy_note(rows_processed):
    mask = constants.PII_MASK_TOKEN
    return f"""# Reviewer Identity Data — Handling Note

## What we do

1. **Display name, email, and phone number all masked, not dropped.**
   `ProfileName`, `CustomerEmail`, and `CustomerPhone` are replaced with a
   fixed placeholder ("{mask}") before anything is embedded. The columns are
   retained (rather than removed) so the schema stays consistent for
   downstream code and so it's auditable that the field existed and was
   deliberately redacted, not silently absent. We deliberately do NOT replace
   `ProfileName` with a derived pseudonym — `UserId` (Amazon's own opaque
   identifier, already present in the raw data) already lets us tell "same
   customer, multiple reviews" apart from "different customers".

2. **Contact info redacted from free text.** Review `Text` and `Summary`
   fields are scanned for email addresses and phone-number-shaped strings
   (reviewers occasionally paste these into review text) and redacted
   before embedding.

3. **`UserId` retained as-is — the only surviving per-customer identifier.**
   This is Amazon's own opaque identifier (e.g. `A3SGXH7AUHU8GW`) — not a
   real name, and not reversible to one without Amazon's internal systems.
   Kept for deduping/joins, never surfaced in chat responses.

4. **`ProductName` / `ProductId` are untouched.** They identify the
   product, not the person, so they're not in scope for this step.

5. **Nothing scrubbed is embedded or indexed.** The vector store is built
   from the *scrubbed* file, not the raw or labeled file.

## What we don't do (and why)

- We don't attempt full PII redaction of arbitrary free text (e.g. a
  reviewer mentioning "my daughter Sarah") — that is an open-ended NER
  problem beyond this project's scope. We scope to the structured
  identity/contact fields and the clearest high-confidence patterns
  (email, phone) in free text.

## Rows processed

{rows_processed} labeled reviews scrubbed as of this run.
"""


def main():
    if not constants.LABELED_REVIEWS_PATH.exists():
        raise DataNotFoundError(
            f"{constants.LABELED_REVIEWS_PATH} not found. Run "
            "src/labeling/label_reviews.py first (even a partial run works)."
        )

    df = pd.read_csv(constants.LABELED_REVIEWS_PATH)
    rows_processed = len(df)

    for column in [c for c in constants.PII_COLUMNS if c in df.columns]:
        df[column] = df[column].apply(mask_value)

    df["Text"] = df["Text"].apply(clean_html).apply(redact_contact_info)
    df["Summary"] = df["Summary"].apply(clean_html).apply(redact_contact_info)

    constants.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    constants.DOCS_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(constants.SCRUBBED_REVIEWS_PATH, index=False)
    constants.PII_POLICY_PATH.write_text(build_policy_note(rows_processed), encoding="utf-8")

    logger.info("Scrubbed %s rows -> %s", rows_processed, constants.SCRUBBED_REVIEWS_PATH)
    logger.info("Policy note written -> %s", constants.PII_POLICY_PATH)


if __name__ == "__main__":
    try:
        main()
    except AppError as error:
        logger.error("%s", error.message)
        sys.exit(1)
    except Exception:
        logger.exception("Scrubbing failed")
        sys.exit(1)
