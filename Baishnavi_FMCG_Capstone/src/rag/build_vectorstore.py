"""
build_vectorstore.py
=====================
Chunks and embeds scrubbed_reviews.csv into a persistent ChromaDB vector
store, using a local sentence-transformers model (no API calls, no cost).

Chunking: one review = one chunk. Reviews are short, self-contained
opinions, so splitting them would break a single thought. Each chunk is
`Summary + ". " + Text`.

Embedded (the vector): Summary + Text.
Stored as metadata (not embedded, but attached to each vector for
filtering): ProductId, ProductName, UserId, Score, Time, sentiment, aspect,
severity, helpfulness counts.

Run from the project root:
    python -m src.rag.build_vectorstore

Re-running rebuilds the collection from scratch (no duplicates).
"""

import os
os.environ.setdefault("LOG_FILE_NAME", "pipeline.log")

import sys

import chromadb
import pandas as pd
from chromadb.utils import embedding_functions
from tqdm import tqdm

from src.config import constants
from src.exceptions import AppError, DataNotFoundError, VectorStoreError
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_chunk_text(row):
    """One review = one chunk: the short Summary headline plus the full Text."""
    summary = str(row["Summary"]) if pd.notna(row["Summary"]) else ""
    text = str(row["Text"]) if pd.notna(row["Text"]) else ""
    if summary and not summary.endswith((".", "!", "?")):
        summary += "."
    return f"{summary} {text}".strip()


def build_metadata(row):
    """Everything here rides alongside the vector for filtering later.
    Chroma metadata values must be str/int/float/bool."""
    return {
        "review_id": int(row["Id"]),
        "product_id": str(row["ProductId"]),
        "product_name": str(row["ProductName"]),
        "user_id": str(row["UserId"]),
        "score": int(row["Score"]),
        "time": int(row["Time"]),
        "sentiment": str(row["sentiment"]),
        "aspect": str(row["aspect"]),
        "severity": int(row["severity"]),
        "helpfulness_numerator": int(row["HelpfulnessNumerator"]),
        "helpfulness_denominator": int(row["HelpfulnessDenominator"]),
    }


def main():
    if not constants.SCRUBBED_REVIEWS_PATH.exists():
        raise DataNotFoundError(
            f"{constants.SCRUBBED_REVIEWS_PATH} not found. Run src/rag/scrub_pii.py first."
        )

    df = pd.read_csv(constants.SCRUBBED_REVIEWS_PATH)
    total_rows = len(df)
    logger.info("Loaded %s scrubbed reviews from %s", total_rows, constants.SCRUBBED_REVIEWS_PATH)

    logger.info("Loading local embedding model: %s (first run downloads it)",
                constants.EMBEDDING_MODEL_NAME)
    try:
        embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=constants.EMBEDDING_MODEL_NAME
        )
    except Exception as error:
        raise VectorStoreError(f"Could not load the embedding model: {error}") from error

    constants.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(constants.VECTORSTORE_DIR))

    # Rebuild from scratch each run so re-running never duplicates rows.
    existing = [collection.name for collection in client.list_collections()]
    if constants.COLLECTION_NAME in existing:
        client.delete_collection(constants.COLLECTION_NAME)

    collection = client.create_collection(
        name=constants.COLLECTION_NAME,
        embedding_function=embedding_fn,
        metadata={"hnsw:space": constants.VECTORSTORE_DISTANCE_SPACE},
    )

    ids = [str(row_id) for row_id in df["Id"].tolist()]
    documents = [build_chunk_text(row) for _, row in df.iterrows()]
    metadatas = [build_metadata(row) for _, row in df.iterrows()]

    batch_size = constants.EMBED_BATCH_SIZE
    logger.info("Embedding and storing %s reviews in batches of %s", total_rows, batch_size)
    for start in tqdm(range(0, total_rows, batch_size), desc="Building vector store"):
        end = start + batch_size
        collection.add(ids=ids[start:end], documents=documents[start:end],
                       metadatas=metadatas[start:end])

    logger.info("Done. %s reviews embedded -> %s", collection.count(), constants.VECTORSTORE_DIR)
    logger.info("Collection name: %s", constants.COLLECTION_NAME)


if __name__ == "__main__":
    try:
        main()
    except AppError as error:
        logger.error("%s", error.message)
        sys.exit(1)
    except Exception:
        logger.exception("Building the vector store failed")
        sys.exit(1)
