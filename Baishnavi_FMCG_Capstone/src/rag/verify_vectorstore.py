"""
verify_vectorstore.py
======================
Sanity-checks the vector store built by build_vectorstore.py. Changes
nothing: it loads the existing collection through the same loader the app
uses (repositories/data_access.py) and runs a few queries so you can check
that retrieval works and metadata filtering behaves correctly.

Run from the project root:
    python -m src.rag.verify_vectorstore
"""

import os
os.environ.setdefault("LOG_FILE_NAME", "pipeline.log")

import sys

from src.config import constants
from src.exceptions import AppError
from src.repositories.data_access import load_vectorstore
from src.utils.logger import get_logger

logger = get_logger(__name__)

DIVIDER = "=" * 70


def preview(document):
    return f"{document[:constants.VERIFY_PREVIEW_CHARS]}..."


def check_semantic_search(collection):
    logger.info(DIVIDER)
    logger.info("TEST 1: Semantic search for '%s'", constants.VERIFY_SEMANTIC_QUERY)
    results = collection.query(
        query_texts=[constants.VERIFY_SEMANTIC_QUERY],
        n_results=constants.VERIFY_RESULT_COUNT,
    )
    for document, meta, distance in zip(
        results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        logger.info("[distance=%.3f] %s | sentiment=%s | severity=%s",
                    distance, meta["product_name"], meta["sentiment"], meta["severity"])
        logger.info("  %s", preview(document))


def check_severity_filter(collection):
    logger.info(DIVIDER)
    logger.info("TEST 2: Metadata filter - severity >= %s", constants.HIGH_SEVERITY_THRESHOLD)
    flagged = collection.get(
        where={"severity": {"$gte": constants.HIGH_SEVERITY_THRESHOLD}},
        limit=constants.VERIFY_FLAGGED_COUNT,
    )
    if not flagged["ids"]:
        logger.info("No reviews with high severity in this sample (plausible for food reviews).")
        return
    for meta, document in zip(flagged["metadatas"], flagged["documents"]):
        logger.info("%s | severity=%s", meta["product_name"], meta["severity"])
        logger.info("  %s", preview(document))


def check_filtered_search(collection):
    logger.info(DIVIDER)
    logger.info("TEST 3: Semantic search + filter - aspect '%s' only", constants.VERIFY_FILTER_ASPECT)
    results = collection.query(
        query_texts=[constants.VERIFY_FILTERED_QUERY],
        n_results=constants.VERIFY_RESULT_COUNT,
        where={"aspect": constants.VERIFY_FILTER_ASPECT},
    )
    if not results["documents"][0]:
        logger.info("No %s-aspect matches for this query in the top results.",
                    constants.VERIFY_FILTER_ASPECT)
        return
    for document, meta in zip(results["documents"][0], results["metadatas"][0]):
        logger.info("%s | aspect=%s | sentiment=%s",
                    meta["product_name"], meta["aspect"], meta["sentiment"])
        logger.info("  %s", preview(document))


def main():
    collection = load_vectorstore()
    logger.info("Collection '%s' loaded. Total reviews: %s",
                constants.COLLECTION_NAME, collection.count())

    check_semantic_search(collection)
    check_severity_filter(collection)
    check_filtered_search(collection)

    logger.info(DIVIDER)
    logger.info("If TEST 1 returned dog-food-relevant results, TEST 2 returned nothing or "
                "genuinely high-severity reviews, and every TEST 3 result says "
                "aspect=%s, the vector store is working correctly.", constants.VERIFY_FILTER_ASPECT)


if __name__ == "__main__":
    try:
        main()
    except AppError as error:
        logger.error("%s", error.message)
        sys.exit(1)
    except Exception:
        logger.exception("Vector store verification failed")
        sys.exit(1)
