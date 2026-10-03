"""Tests for src/rag/build_vectorstore.py. ChromaDB and the embedding model
are replaced with fakes, so nothing is downloaded or written to a real store.
"""

from types import SimpleNamespace

import pandas as pd
import pytest

from src.config import constants
from src.exceptions import DataNotFoundError, VectorStoreError
from src.rag import build_vectorstore


def make_row(**overrides):
    row = {
        "Id": 1, "ProductId": "P1", "ProductName": "Chicken Formula", "UserId": "U1",
        "Score": 4, "Time": 1_356_998_400, "Summary": "Great", "Text": "My dog loves it.",
        "HelpfulnessNumerator": 2, "HelpfulnessDenominator": 3,
        "sentiment": "positive", "aspect": "taste", "severity": 0,
    }
    row.update(overrides)
    return pd.Series(row)


class TestBuildChunkText:
    def test_adds_a_full_stop_after_a_bare_summary(self):
        assert build_vectorstore.build_chunk_text(make_row()) == "Great. My dog loves it."

    @pytest.mark.parametrize("summary", ["Great!", "Great?", "Great."])
    def test_keeps_existing_end_punctuation(self, summary):
        chunk = build_vectorstore.build_chunk_text(make_row(Summary=summary))
        assert chunk == f"{summary} My dog loves it."

    def test_missing_summary_leaves_just_the_text(self):
        assert build_vectorstore.build_chunk_text(make_row(Summary=float("nan"))) == "My dog loves it."

    def test_missing_text_leaves_just_the_summary(self):
        assert build_vectorstore.build_chunk_text(make_row(Text=float("nan"))) == "Great."

    def test_both_missing_gives_an_empty_chunk(self):
        row = make_row(Summary=float("nan"), Text=float("nan"))
        assert build_vectorstore.build_chunk_text(row) == ""


class TestBuildMetadata:
    def test_maps_every_field_with_chroma_safe_types(self):
        metadata = build_vectorstore.build_metadata(make_row())
        assert metadata == {
            "review_id": 1, "product_id": "P1", "product_name": "Chicken Formula",
            "user_id": "U1", "score": 4, "time": 1_356_998_400, "sentiment": "positive",
            "aspect": "taste", "severity": 0, "helpfulness_numerator": 2,
            "helpfulness_denominator": 3,
        }
        assert all(type(value) in (int, str) for value in metadata.values())


class FakeCollection:
    def __init__(self):
        self.added = []

    def add(self, ids, documents, metadatas):
        self.added.append((ids, documents, metadatas))

    def count(self):
        return sum(len(ids) for ids, _docs, _meta in self.added)


class FakeChromaClient:
    def __init__(self, existing_names=()):
        self.existing = [SimpleNamespace(name=name) for name in existing_names]
        self.deleted = []
        self.created = {}
        self.collection = FakeCollection()

    def list_collections(self):
        return self.existing

    def delete_collection(self, name):
        self.deleted.append(name)

    def create_collection(self, name, embedding_function, metadata):
        self.created = {"name": name, "embedding_function": embedding_function, "metadata": metadata}
        return self.collection


@pytest.fixture
def store_env(tmp_path, monkeypatch):
    csv_path = tmp_path / "scrubbed.csv"
    rows = [make_row(Id=n, ProductId=f"P{n}") for n in range(1, 6)]
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    monkeypatch.setattr(constants, "SCRUBBED_REVIEWS_PATH", csv_path)
    monkeypatch.setattr(constants, "VECTORSTORE_DIR", tmp_path / "vectorstore")
    monkeypatch.setattr(constants, "EMBED_BATCH_SIZE", 2)

    def install(client, embedder="fake-embedder"):
        monkeypatch.setattr(build_vectorstore, "chromadb",
                            SimpleNamespace(PersistentClient=lambda path: client))
        if isinstance(embedder, Exception):
            def failing(model_name):
                raise embedder
            embedding = failing
        else:
            embedding = lambda model_name: embedder  # noqa: E731
        monkeypatch.setattr(build_vectorstore, "embedding_functions",
                            SimpleNamespace(SentenceTransformerEmbeddingFunction=embedding))

    return SimpleNamespace(install=install, csv_path=csv_path)


class TestMain:
    def test_missing_input_file_is_reported(self, tmp_path, monkeypatch):
        monkeypatch.setattr(constants, "SCRUBBED_REVIEWS_PATH", tmp_path / "missing.csv")
        with pytest.raises(DataNotFoundError):
            build_vectorstore.main()

    def test_embedding_model_failure_becomes_vectorstore_error(self, store_env):
        store_env.install(FakeChromaClient(), embedder=RuntimeError("no model"))
        with pytest.raises(VectorStoreError):
            build_vectorstore.main()

    def test_stores_every_review_in_batches(self, store_env):
        client = FakeChromaClient()
        store_env.install(client)
        build_vectorstore.main()

        assert client.deleted == []
        assert client.created["name"] == constants.COLLECTION_NAME
        assert client.created["embedding_function"] == "fake-embedder"
        assert client.created["metadata"] == {"hnsw:space": constants.VECTORSTORE_DISTANCE_SPACE}
        batches = client.collection.added
        assert [len(ids) for ids, _d, _m in batches] == [2, 2, 1]  # 5 rows, batch size 2
        assert batches[0][0] == ["1", "2"]
        assert batches[0][1][0] == "Great. My dog loves it."
        assert batches[0][2][0]["product_id"] == "P1"

    def test_an_existing_collection_is_deleted_first(self, store_env):
        client = FakeChromaClient(existing_names=[constants.COLLECTION_NAME, "other"])
        store_env.install(client)
        build_vectorstore.main()
        assert client.deleted == [constants.COLLECTION_NAME]
