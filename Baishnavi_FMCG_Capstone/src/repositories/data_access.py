"""
data_access.py
====================
Single shared loader for scrubbed_reviews.csv and for the ChromaDB
vector store, so the tools never re-read the CSV or re-open the index on
every call.

The embedding model is loaded once per process and kept in memory. If the
load FAILS, the failure is remembered for a cooldown period
(VECTORSTORE_RETRY_COOLDOWN_SECONDS) so a broken model is not reloaded
again and again on every question.

Dates: `Time` is a Unix epoch column. It is converted with `unit="s",
utc=True` and then made timezone-naive -- one fixed, explicit rule, used
everywhere in this file and by every tool. Previously, different tools
parsed dates in different ways (one used pandas' local-time default,
another used UTC), so the same date range could return different rows
in different tools. `end_date` filters are inclusive of the whole day.
"""

import os
os.environ.setdefault("HF_HUB_OFFLINE", "1")

import threading
import time
from functools import lru_cache

import chromadb
import pandas as pd
from chromadb.utils import embedding_functions

from src.config import constants
from src.exceptions import DataNotFoundError, InvalidInputError, VectorStoreError
from src.utils.logger import get_logger

logger = get_logger(__name__)

_vectorstore_lock = threading.Lock()
_vectorstore_state = {"collection": None, "failed_at": None, "error": None}


def _drop_unverified_labels(df):
    """Keeps only rows whose labels the model really produced (label_status
    == "ok"). Rows marked "fallback" (the whole batch failed) or "unverified"
    (the model skipped that review) carry placeholder labels -- neutral /
    other / severity 0 -- not real ones. Counting them would skew sentiment
    trends and could hide a genuine safety issue behind severity 0. They stay
    in the CSV for audit; they just never reach the analytics.
    A file with no label_status column (older data) is left untouched."""
    column = constants.LABEL_STATUS_COLUMN
    if column not in df.columns:
        return df
    keep = df[column] == constants.LABEL_STATUS_OK
    dropped = int((~keep).sum())
    if not keep.any():
        raise DataNotFoundError(
            f"Every row in {constants.SCRUBBED_REVIEWS_PATH.name} has a fallback/unverified "
            "label, so there is nothing reliable to analyse. Re-run the labeling step."
        )
    if dropped:
        logger.warning(
            "Excluded %s of %s review(s) with fallback/unverified labels from the analytics "
            "(kept in the CSV for audit).", dropped, len(df),
        )
    return df[keep].reset_index(drop=True)


@lru_cache(maxsize=1)
def load_reviews():
    if not constants.SCRUBBED_REVIEWS_PATH.exists():
        raise DataNotFoundError(
            f"Review data file not found: {constants.SCRUBBED_REVIEWS_PATH}. "
            "Run the labeling, scrubbing and embedding scripts first."
        )
    try:
        df = pd.read_csv(constants.SCRUBBED_REVIEWS_PATH)
        missing = [c for c in constants.REQUIRED_REVIEW_COLUMNS if c not in df.columns]
        if missing:
            raise DataNotFoundError(
                f"{constants.SCRUBBED_REVIEWS_PATH.name} is missing required column(s): "
                f"{', '.join(missing)}. Re-run the labeling/scrubbing pipeline."
            )
        df = _drop_unverified_labels(df)
        # One fixed rule for every date in the project: parse Time as UTC
        # epoch seconds, then drop the tz so it compares cleanly against
        # the naive dates typed into API requests.
        df["datetime"] = pd.to_datetime(df["Time"], unit="s", utc=True).dt.tz_localize(None)
    except DataNotFoundError:
        raise
    except (ValueError, KeyError, pd.errors.ParserError) as error:
        logger.exception("Could not read %s", constants.SCRUBBED_REVIEWS_PATH)
        raise DataNotFoundError("The review data file could not be read.") from error
    logger.info("Loaded %s reviews from %s (date range %s to %s)",
                len(df), constants.SCRUBBED_REVIEWS_PATH.name,
                df["datetime"].min().date(), df["datetime"].max().date())
    return df


def get_dataset_today():
    """Returns the most recent review date in the dataset, as a date object.
    The agent anchors 'today'/'this week'/'last month' to this instead of
    the real calendar date, because the review data itself is from years
    ago -- resolving relative dates against the real 'today' would always
    return empty results."""
    df = load_reviews()
    return df["datetime"].max().date()


def _parse_date_arg(value, arg_name):
    try:
        return pd.to_datetime(value)
    except (ValueError, TypeError) as error:
        raise InvalidInputError(
            f"Invalid {arg_name}: {value!r}. Use an ISO date like YYYY-MM-DD."
        ) from error


def filter_by_date(df, start_date, end_date):
    """Filters to [start_date 00:00, end_date 23:59:59.999999] inclusive.
    A plain `<= end_date` (no time component) would exclude that entire
    day, since pandas parses a bare date as midnight."""
    if start_date:
        df = df[df["datetime"] >= _parse_date_arg(start_date, "start_date")]
    if end_date:
        end = _parse_date_arg(end_date, "end_date") + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
        df = df[df["datetime"] <= end]
    return df


def load_vectorstore():
    """Opens the persistent Chroma collection built by
    src/rag/build_vectorstore.py. The embedding model is loaded once per
    process; a failed load is remembered and not retried during the cooldown."""
    collection = _vectorstore_state["collection"]
    if collection is not None:
        return collection

    with _vectorstore_lock:
        collection = _vectorstore_state["collection"]
        if collection is not None:
            return collection

        failed_at = _vectorstore_state["failed_at"]
        cooldown = constants.VECTORSTORE_RETRY_COOLDOWN_SECONDS
        if failed_at is not None and time.monotonic() - failed_at < cooldown:
            remaining = round(cooldown - (time.monotonic() - failed_at))
            raise VectorStoreError(
                "The review search index failed to load earlier and is not being "
                f"retried yet ({remaining}s remaining). Do not retry this search.",
                details=_vectorstore_state["error"],
            )

        try:
            logger.info("Loading vector store from %s", constants.VECTORSTORE_DIR)
            client = chromadb.PersistentClient(path=str(constants.VECTORSTORE_DIR))
            logger.info("Loading embedding model %s (slow step, once per process)",
                        constants.EMBEDDING_MODEL_NAME)
            embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=constants.EMBEDDING_MODEL_NAME
            )
            collection = client.get_collection(
                name=constants.COLLECTION_NAME, embedding_function=embedding_fn
            )
        except Exception as error:
            _vectorstore_state["failed_at"] = time.monotonic()
            _vectorstore_state["error"] = f"{type(error).__name__}: {error}"
            logger.exception("Vector store load failed")
            raise VectorStoreError("The review search index could not be loaded.") from error

        _vectorstore_state["collection"] = collection
        _vectorstore_state["failed_at"] = None
        _vectorstore_state["error"] = None
        logger.info("Vector store ready (%s reviews)", collection.count())
        return collection


def reset_caches_for_tests():
    """Test-only helper: clears the module-level caches so each test starts clean."""
    load_reviews.cache_clear()
    _vectorstore_state.update(collection=None, failed_at=None, error=None)

