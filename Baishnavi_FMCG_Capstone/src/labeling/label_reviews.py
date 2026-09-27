"""
label_reviews.py
====================
Labels each review with:
  - sentiment : positive | negative | neutral
  - aspect    : taste | packaging | price | availability | other
  - severity  : 0-5  (0 = no safety/quality concern, 5 = urgent safety issue)

Uses a Groq-hosted model (constants.LABEL_MODEL_NAME), sending reviews in
batches to stay inside the free-tier rate limits, with up to
LABEL_MAX_RETRIES retries (with backoff) per batch before falling back to
neutral/other/0 for that batch. Every row's `label_status` column records
whether its labels came from the model ("ok"), a parse/validation failure
("fallback"), or -- if the model omitted an id from its response --
("unverified"), so mislabeled rows are visible in the data rather than
silently blended in as if they were "neutral, severity 0" reviews.

Setup: put GROQ_API_KEY=your_key in the .env file in the project root.

Run from the project root:
    python -m src.labeling.label_reviews --input sample_reviews.csv

Re-running the same command resumes from the checkpoint, so it is safe to
interrupt or to re-run after hitting a rate limit.
"""

import os
os.environ.setdefault("LOG_FILE_NAME", "pipeline.log")

import argparse
import json
import sys
import time

import pandas as pd
from groq import Groq
from tqdm import tqdm

from src.config import constants
from src.config.prompts import LABEL_FEW_SHOT, LABEL_SYSTEM_PROMPT
from src.exceptions import AppError, ConfigError, DataNotFoundError
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_batch_prompt(batch_texts):
    numbered = "\n".join(f"{i + 1}. {text}" for i, text in enumerate(batch_texts))
    return f"{LABEL_FEW_SHOT}\nNow label these reviews:\n\n{numbered}"


def _validate_label(label):
    """Returns a cleaned label dict, or None if it fails validation."""
    if not isinstance(label, dict):
        return None
    sentiment = label.get("sentiment")
    aspect = label.get("aspect")
    severity = label.get("severity")
    if sentiment not in constants.SENTIMENT_LABELS:
        return None
    if aspect not in constants.ASPECTS:
        return None
    if not isinstance(severity, int) or not constants.SEVERITY_MIN <= severity <= constants.SEVERITY_MAX:
        return None
    return {"sentiment": sentiment, "aspect": aspect, "severity": severity}


def call_model_once(client, batch_texts):
    """One attempt. Returns a parsed JSON list, or raises on any failure
    (network error, non-JSON output, or JSON that isn't a list) so the
    caller's retry loop can distinguish 'try again' from 'give up'."""
    response = client.chat.completions.create(
        model=constants.LABEL_MODEL_NAME,
        messages=[
            {"role": "system", "content": LABEL_SYSTEM_PROMPT},
            {"role": "user", "content": build_batch_prompt(batch_texts)},
        ],
        temperature=constants.LABEL_TEMPERATURE,
        max_tokens=constants.LABEL_MAX_TOKENS,
    )
    text = (response.choices[0].message.content or "").strip()
    text = text.replace("```json", "").replace("```", "").strip()
    parsed = json.loads(text)  # raises json.JSONDecodeError on bad output
    if not isinstance(parsed, list):
        raise ValueError("Model response was valid JSON but not a list")
    return parsed


def call_model_with_retries(client, batch_texts):
    """Retries transient failures (network errors, malformed JSON) up to
    LABEL_MAX_RETRIES times with backoff. Returns (labels_by_id, status):
    status is 'ok' if the model responded validly, 'fallback' if every
    attempt failed."""
    last_error = None
    for attempt in range(1, constants.LABEL_MAX_RETRIES + 1):
        try:
            raw_labels = call_model_once(client, batch_texts)
            return raw_labels, "ok"
        except (json.JSONDecodeError, ValueError) as error:
            last_error = error
            logger.warning("Batch parse failed (attempt %s/%s): %s",
                           attempt, constants.LABEL_MAX_RETRIES, error)
        except Exception as error:  # network/API errors: worth retrying too
            last_error = error
            logger.warning("Batch request failed (attempt %s/%s): %s",
                           attempt, constants.LABEL_MAX_RETRIES, error)
        if attempt < constants.LABEL_MAX_RETRIES:
            time.sleep(constants.LABEL_RETRY_BACKOFF_SECONDS * attempt)

    logger.error("Batch failed after %s attempts, using fallback labels. Last error: %s",
                constants.LABEL_MAX_RETRIES, last_error)
    return [], "fallback"


def labels_for_batch(client, batch_texts):
    """Returns one validated label dict per input text, in order, plus a
    parallel list of per-row statuses (constants.LABEL_STATUS_*)."""
    raw_labels, batch_status = call_model_with_retries(client, batch_texts)
    by_id = {item.get("id"): item for item in raw_labels if isinstance(item, dict)}

    labels, statuses = [], []
    for position in range(len(batch_texts)):
        if batch_status == "fallback":
            labels.append(dict(constants.LABEL_FALLBACK))
            statuses.append(constants.LABEL_STATUS_FALLBACK)
            continue

        raw = by_id.get(position + 1)
        if raw is None:
            labels.append(dict(constants.LABEL_FALLBACK))
            statuses.append(constants.LABEL_STATUS_UNVERIFIED)
            continue

        validated = _validate_label(raw)
        if validated is None:
            labels.append(dict(constants.LABEL_FALLBACK))
            statuses.append(constants.LABEL_STATUS_FALLBACK)
        else:
            labels.append(validated)
            statuses.append(constants.LABEL_STATUS_OK)

    return labels, statuses


def load_checkpoint():
    if constants.LABEL_CHECKPOINT_PATH.exists():
        return json.loads(constants.LABEL_CHECKPOINT_PATH.read_text())["next_index"]
    return 0


def save_checkpoint(next_index):
    constants.LABEL_CHECKPOINT_PATH.write_text(json.dumps({"next_index": next_index}))


def append_results(rows):
    df = pd.DataFrame(rows)
    write_header = not constants.LABELED_REVIEWS_PATH.exists()
    df.to_csv(constants.LABELED_REVIEWS_PATH, mode="a", header=write_header, index=False)


def main(input_csv, text_column, batch_size, daily_budget):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ConfigError("GROQ_API_KEY is not set. Add it to the .env file in the project root.")
    client = Groq(api_key=api_key)

    input_path = constants.RAW_DIR / input_csv
    if not input_path.exists():
        raise DataNotFoundError(f"Input file not found: {input_path}")

    constants.PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(input_path)
    total_rows = len(df)
    start_index = load_checkpoint()

    if start_index >= total_rows:
        logger.info("All %s rows already labeled. Nothing to do.", total_rows)
        return

    logger.info("Resuming from row %s/%s", start_index, total_rows)

    requests_used = 0
    idx = start_index
    fallback_count = 0

    progress = tqdm(total=total_rows, initial=start_index, desc="Labeling reviews")
    while idx < total_rows and requests_used < daily_budget:
        batch_df = df.iloc[idx: idx + batch_size]
        batch_texts = batch_df[text_column].astype(str).tolist()

        labels, statuses = labels_for_batch(client, batch_texts)
        requests_used += 1

        rows_out = []
        for (_, row), label, status in zip(batch_df.iterrows(), labels, statuses):
            row_dict = row.to_dict()
            row_dict["sentiment"] = label["sentiment"]
            row_dict["aspect"] = label["aspect"]
            row_dict["severity"] = label["severity"]
            row_dict[constants.LABEL_STATUS_COLUMN] = status
            rows_out.append(row_dict)
            if status != constants.LABEL_STATUS_OK:
                fallback_count += 1

        append_results(rows_out)
        idx += len(batch_df)
        save_checkpoint(idx)
        progress.update(len(batch_df))
        time.sleep(constants.LABEL_SECONDS_BETWEEN_REQUESTS)

    progress.close()

    remaining = total_rows - idx
    if fallback_count:
        logger.warning("%s row(s) used fallback/unverified labels -- filter on "
                       "%s != '%s' to find and re-check them.",
                       fallback_count, constants.LABEL_STATUS_COLUMN, constants.LABEL_STATUS_OK)
    if remaining > 0:
        logger.info("Stopped at row %s/%s (%s remaining). Re-run the same command to continue.",
                    idx, total_rows, remaining)
    else:
        logger.info("Done. All %s rows labeled -> %s", total_rows, constants.LABELED_REVIEWS_PATH)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="CSV filename inside data/raw/")
    parser.add_argument("--text-column", default=constants.LABEL_DEFAULT_TEXT_COLUMN)
    parser.add_argument("--batch-size", type=int, default=constants.LABEL_DEFAULT_BATCH_SIZE,
                        help="Reviews per API request")
    parser.add_argument("--daily-budget", type=int, default=constants.LABEL_DAILY_REQUEST_BUDGET,
                        help="Max requests to use in this run (stay under the daily cap)")
    args = parser.parse_args()

    try:
        main(args.input, args.text_column, args.batch_size, args.daily_budget)
    except AppError as error:
        logger.error("%s", error.message)
        sys.exit(1)
    except Exception:
        logger.exception("Labeling failed")
        sys.exit(1)
