"""Tests for src/rag/verify_vectorstore.py, using a fake collection that
records the queries it receives. No real vector store is opened.
"""

from src.config import constants
from src.rag import verify_vectorstore


class FakeCollection:
    def __init__(self, with_results=True):
        self.with_results = with_results
        self.queries = []
        self.gets = []

    def count(self):
        return 3

    def query(self, **kwargs):
        self.queries.append(kwargs)
        if not self.with_results:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]]}
        meta = {"product_name": "Beef Formula", "sentiment": "negative",
                "severity": 2, "aspect": "packaging"}
        return {"documents": [["a leaking bag", "a torn bag"]], "metadatas": [[meta, meta]],
                "distances": [[0.11, 0.22]]}

    def get(self, **kwargs):
        self.gets.append(kwargs)
        if not self.with_results:
            return {"ids": [], "metadatas": [], "documents": []}
        meta = {"product_name": "Salmon Formula", "severity": 5}
        return {"ids": ["5"], "metadatas": [meta], "documents": ["found mold inside"]}


class TestPreview:
    def test_truncates_long_documents(self):
        shown = verify_vectorstore.preview("x" * 500)
        assert shown == "x" * constants.VERIFY_PREVIEW_CHARS + "..."

    def test_short_documents_still_get_the_ellipsis(self):
        assert verify_vectorstore.preview("short") == "short..."


class TestChecks:
    def test_semantic_search_uses_the_configured_query(self):
        collection = FakeCollection()
        verify_vectorstore.check_semantic_search(collection)
        assert collection.queries == [{
            "query_texts": [constants.VERIFY_SEMANTIC_QUERY],
            "n_results": constants.VERIFY_RESULT_COUNT,
        }]

    def test_severity_filter_asks_for_high_severity_reviews(self):
        collection = FakeCollection()
        verify_vectorstore.check_severity_filter(collection)
        assert collection.gets[0]["where"] == {
            "severity": {"$gte": constants.HIGH_SEVERITY_THRESHOLD}
        }
        assert collection.gets[0]["limit"] == constants.VERIFY_FLAGGED_COUNT

    def test_severity_filter_handles_no_matches(self):
        collection = FakeCollection(with_results=False)
        verify_vectorstore.check_severity_filter(collection)  # should only log
        assert len(collection.gets) == 1

    def test_filtered_search_restricts_to_one_aspect(self):
        collection = FakeCollection()
        verify_vectorstore.check_filtered_search(collection)
        assert collection.queries[0]["where"] == {"aspect": constants.VERIFY_FILTER_ASPECT}
        assert collection.queries[0]["query_texts"] == [constants.VERIFY_FILTERED_QUERY]

    def test_filtered_search_handles_no_matches(self):
        collection = FakeCollection(with_results=False)
        verify_vectorstore.check_filtered_search(collection)  # should only log
        assert len(collection.queries) == 1


class TestMain:
    def test_runs_all_three_checks(self, monkeypatch):
        collection = FakeCollection()
        monkeypatch.setattr(verify_vectorstore, "load_vectorstore", lambda: collection)
        verify_vectorstore.main()
        assert len(collection.queries) == 2  
        assert len(collection.gets) == 1     
