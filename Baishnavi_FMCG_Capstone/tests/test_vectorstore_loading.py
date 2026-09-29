"""Tests for load_vectorstore() in src/repositories/data_access.py: the
success path, the failure path, and the cooldown that stops a broken model
from being reloaded on every question. chromadb.PersistentClient and
SentenceTransformerEmbeddingFunction are replaced with fakes -- no real
model download or disk-backed Chroma client involved.
"""

import pytest

from src.exceptions import DataNotFoundError, VectorStoreError
from src.repositories import data_access


class FakeCollection:
    def __init__(self, count=5000):
        self._count = count

    def count(self):
        return self._count


@pytest.fixture(autouse=True)
def clean_vectorstore_state():
    data_access.reset_caches_for_tests()
    yield
    data_access.reset_caches_for_tests()


class TestLoadVectorstoreSuccess:
    def test_returns_the_collection_from_the_client(self, monkeypatch):
        fake_collection = FakeCollection()

        class FakeClient:
            def get_collection(self, name, embedding_function):
                return fake_collection

        monkeypatch.setattr(data_access.chromadb, "PersistentClient", lambda path: FakeClient())
        monkeypatch.setattr(
            data_access.embedding_functions, "SentenceTransformerEmbeddingFunction",
            lambda model_name: object(),
        )

        result = data_access.load_vectorstore()
        assert result is fake_collection

    def test_second_call_reuses_the_cached_collection(self, monkeypatch):
        build_count = {"n": 0}

        class FakeClient:
            def get_collection(self, name, embedding_function):
                build_count["n"] += 1
                return FakeCollection()

        monkeypatch.setattr(data_access.chromadb, "PersistentClient", lambda path: FakeClient())
        monkeypatch.setattr(
            data_access.embedding_functions, "SentenceTransformerEmbeddingFunction",
            lambda model_name: object(),
        )

        data_access.load_vectorstore()
        data_access.load_vectorstore()
        assert build_count["n"] == 1  # the model/client only ever loaded once


class TestLoadVectorstoreFailure:
    def test_a_broken_embedding_model_raises_vectorstore_error(self, monkeypatch):
        monkeypatch.setattr(data_access.chromadb, "PersistentClient", lambda path: object())

        def blow_up(model_name):
            raise ImportError("DLL load failed while importing lib")

        monkeypatch.setattr(data_access.embedding_functions, "SentenceTransformerEmbeddingFunction", blow_up)

        with pytest.raises(VectorStoreError):
            data_access.load_vectorstore()

    def test_a_second_call_during_the_cooldown_fails_fast_without_retrying(self, monkeypatch):
        attempts = {"n": 0}

        def blow_up(model_name):
            attempts["n"] += 1
            raise RuntimeError("boom")

        monkeypatch.setattr(data_access.chromadb, "PersistentClient", lambda path: object())
        monkeypatch.setattr(data_access.embedding_functions, "SentenceTransformerEmbeddingFunction", blow_up)

        with pytest.raises(VectorStoreError):
            data_access.load_vectorstore()
        with pytest.raises(VectorStoreError):
            data_access.load_vectorstore()

        assert attempts["n"] == 1  # the second call hit the cooldown, not a real retry

    def test_cooldown_expiring_allows_a_fresh_attempt(self, monkeypatch):
        monkeypatch.setattr(data_access.chromadb, "PersistentClient", lambda path: object())
        monkeypatch.setattr(
            data_access.embedding_functions, "SentenceTransformerEmbeddingFunction",
            lambda model_name: (_ for _ in ()).throw(RuntimeError("boom")),
        )
        with pytest.raises(VectorStoreError):
            data_access.load_vectorstore()

        # Simulate the cooldown having already elapsed.
        data_access._vectorstore_state["failed_at"] -= data_access.constants.VECTORSTORE_RETRY_COOLDOWN_SECONDS + 1

        fake_collection = FakeCollection()

        class FakeClient:
            def get_collection(self, name, embedding_function):
                return fake_collection

        monkeypatch.setattr(data_access.chromadb, "PersistentClient", lambda path: FakeClient())
        monkeypatch.setattr(
            data_access.embedding_functions, "SentenceTransformerEmbeddingFunction",
            lambda model_name: object(),
        )

        assert data_access.load_vectorstore() is fake_collection


class TestLoadReviewsColumnValidation:
    def test_missing_required_column_raises_a_clear_error(self, tmp_path, monkeypatch):
        import pandas as pd
        # Missing the required "severity" column.
        df = pd.DataFrame({
            "Id": [1], "ProductId": ["P1"], "ProductName": ["X"], "Score": [5],
            "Time": [1356998400], "Summary": ["s"], "Text": ["t"], "sentiment": ["positive"],
            "aspect": ["taste"],
        })
        path = tmp_path / "scrubbed_reviews.csv"
        df.to_csv(path, index=False)
        monkeypatch.setattr(data_access.constants, "SCRUBBED_REVIEWS_PATH", path)
        data_access.reset_caches_for_tests()

        with pytest.raises(DataNotFoundError, match="severity"):
            data_access.load_reviews()