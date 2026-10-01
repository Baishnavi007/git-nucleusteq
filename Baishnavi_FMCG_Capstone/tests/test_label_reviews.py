"""Tests for src/labeling/label_reviews.py. The Groq client is a fake that
returns queued responses, so nothing here calls an API or really sleeps.
"""

import json
from types import SimpleNamespace

import pandas as pd
import pytest

from src.config import constants
from src.exceptions import ConfigError, DataNotFoundError
from src.labeling import label_reviews


class FakeClient:
    """Mimics client.chat.completions.create(...): each call pops the next
    queued item, which is either response text or an Exception to raise."""

    def __init__(self, items):
        self.items = list(items)
        self.calls = 0
        self.last_kwargs = None
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.calls += 1
        self.last_kwargs = kwargs
        item = self.items.pop(0)
        if isinstance(item, Exception):
            raise item
        message = SimpleNamespace(content=item)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def good(position, sentiment="negative", aspect="packaging", severity=2):
    return {"id": position, "sentiment": sentiment, "aspect": aspect, "severity": severity}


@pytest.fixture(autouse=True)
def no_sleeping(monkeypatch):
    sleeps = []
    monkeypatch.setattr(label_reviews.time, "sleep", lambda seconds: sleeps.append(seconds))
    return sleeps


class TestBuildBatchPrompt:
    def test_numbers_each_review(self):
        prompt = label_reviews.build_batch_prompt(["first", "second"])
        assert "1. first" in prompt and "2. second" in prompt

    def test_includes_the_few_shot_examples(self):
        assert label_reviews.LABEL_FEW_SHOT in label_reviews.build_batch_prompt(["x"])


class TestValidateLabel:
    def test_valid_label_is_cleaned_to_three_fields(self):
        raw = {"id": 4, "sentiment": "positive", "aspect": "taste", "severity": 0, "extra": "x"}
        assert label_reviews._validate_label(raw) == {
            "sentiment": "positive", "aspect": "taste", "severity": 0,
        }

    @pytest.mark.parametrize("bad", [
        None,
        "not a dict",
        {"sentiment": "angry", "aspect": "taste", "severity": 1},
        {"sentiment": "positive", "aspect": "colour", "severity": 1},
        {"sentiment": "positive", "aspect": "taste", "severity": "high"},
        {"sentiment": "positive", "aspect": "taste", "severity": 99},
        {"sentiment": "positive", "aspect": "taste", "severity": -1},
        {"sentiment": "positive", "aspect": "taste"},
    ])
    def test_invalid_labels_return_none(self, bad):
        assert label_reviews._validate_label(bad) is None


class TestCallModelOnce:
    def test_parses_a_json_list(self):
        client = FakeClient([json.dumps([good(1)])])
        assert label_reviews.call_model_once(client, ["text"]) == [good(1)]

    def test_strips_markdown_code_fences(self):
        client = FakeClient(["```json\n" + json.dumps([good(1)]) + "\n```"])
        assert label_reviews.call_model_once(client, ["text"]) == [good(1)]

    def test_sends_the_configured_model_and_prompt(self):
        client = FakeClient(["[]"])
        label_reviews.call_model_once(client, ["some review"])
        assert client.last_kwargs["model"] == constants.LABEL_MODEL_NAME
        assert "some review" in client.last_kwargs["messages"][1]["content"]

    def test_non_json_output_raises(self):
        with pytest.raises(json.JSONDecodeError):
            label_reviews.call_model_once(FakeClient(["not json at all"]), ["x"])

    def test_empty_response_raises(self):
        with pytest.raises(json.JSONDecodeError):
            label_reviews.call_model_once(FakeClient([None]), ["x"])

    def test_json_that_is_not_a_list_raises(self):
        with pytest.raises(ValueError):
            label_reviews.call_model_once(FakeClient(['{"id": 1}']), ["x"])


class TestCallModelWithRetries:
    def test_first_success_needs_no_retry(self, no_sleeping):
        client = FakeClient([json.dumps([good(1)])])
        labels, status = label_reviews.call_model_with_retries(client, ["x"])
        assert status == "ok" and labels == [good(1)]
        assert client.calls == 1 and no_sleeping == []

    def test_retries_after_malformed_json_then_succeeds(self, no_sleeping):
        client = FakeClient(["garbage", json.dumps([good(1)])])
        _labels, status = label_reviews.call_model_with_retries(client, ["x"])
        assert status == "ok"
        assert client.calls == 2
        assert no_sleeping == [constants.LABEL_RETRY_BACKOFF_SECONDS]

    def test_retries_after_a_network_error(self):
        client = FakeClient([ConnectionError("network down"), json.dumps([good(1)])])
        assert label_reviews.call_model_with_retries(client, ["x"])[1] == "ok"

    def test_gives_up_after_the_maximum_attempts(self, no_sleeping):
        client = FakeClient(["bad"] * constants.LABEL_MAX_RETRIES)
        labels, status = label_reviews.call_model_with_retries(client, ["x"])
        assert (labels, status) == ([], "fallback")
        assert client.calls == constants.LABEL_MAX_RETRIES
        assert len(no_sleeping) == constants.LABEL_MAX_RETRIES - 1


class TestLabelsForBatch:
    def test_all_rows_ok(self):
        client = FakeClient([json.dumps([good(1), good(2, "positive", "taste", 0)])])
        labels, statuses = label_reviews.labels_for_batch(client, ["a", "b"])
        assert statuses == [constants.LABEL_STATUS_OK] * 2
        assert labels[1] == {"sentiment": "positive", "aspect": "taste", "severity": 0}

    def test_total_failure_marks_every_row_as_fallback(self):
        client = FakeClient(["bad"] * constants.LABEL_MAX_RETRIES)
        labels, statuses = label_reviews.labels_for_batch(client, ["a", "b"])
        assert statuses == [constants.LABEL_STATUS_FALLBACK] * 2
        assert labels == [constants.LABEL_FALLBACK] * 2

    def test_an_id_missing_from_the_response_is_unverified(self):
        client = FakeClient([json.dumps([good(1)])])  # model forgot id 2
        _labels, statuses = label_reviews.labels_for_batch(client, ["a", "b"])
        assert statuses == [constants.LABEL_STATUS_OK, constants.LABEL_STATUS_UNVERIFIED]

    def test_an_invalid_label_falls_back_for_that_row_only(self):
        broken = {"id": 2, "sentiment": "angry", "aspect": "taste", "severity": 1}
        client = FakeClient([json.dumps([good(1), broken])])
        labels, statuses = label_reviews.labels_for_batch(client, ["a", "b"])
        assert statuses == [constants.LABEL_STATUS_OK, constants.LABEL_STATUS_FALLBACK]
        assert labels[1] == constants.LABEL_FALLBACK

    def test_non_dict_items_in_the_response_are_ignored(self):
        client = FakeClient([json.dumps(["junk", good(1)])])
        _labels, statuses = label_reviews.labels_for_batch(client, ["a"])
        assert statuses == [constants.LABEL_STATUS_OK]


class TestCheckpointAndResults:
    @pytest.fixture(autouse=True)
    def temp_paths(self, tmp_path, monkeypatch):
        monkeypatch.setattr(constants, "LABEL_CHECKPOINT_PATH", tmp_path / "checkpoint.json")
        monkeypatch.setattr(constants, "LABELED_REVIEWS_PATH", tmp_path / "labeled.csv")

    def test_no_checkpoint_means_start_from_zero(self):
        assert label_reviews.load_checkpoint() == 0

    def test_checkpoint_round_trips(self):
        label_reviews.save_checkpoint(45)
        assert label_reviews.load_checkpoint() == 45

    def test_results_append_with_a_single_header(self):
        label_reviews.append_results([{"Id": 1, "sentiment": "positive"}])
        label_reviews.append_results([{"Id": 2, "sentiment": "negative"}])
        saved = pd.read_csv(constants.LABELED_REVIEWS_PATH)
        assert saved["Id"].tolist() == [1, 2]


class TestMain:
    @pytest.fixture
    def workspace(self, tmp_path, monkeypatch):
        raw_dir = tmp_path / "raw"
        raw_dir.mkdir()
        processed_dir = tmp_path / "processed"
        monkeypatch.setattr(constants, "RAW_DIR", raw_dir)
        monkeypatch.setattr(constants, "PROCESSED_DIR", processed_dir)
        monkeypatch.setattr(constants, "LABEL_CHECKPOINT_PATH", processed_dir / "checkpoint.json")
        monkeypatch.setattr(constants, "LABELED_REVIEWS_PATH", processed_dir / "labeled.csv")
        monkeypatch.setenv("GROQ_API_KEY", "test-key")
        pd.DataFrame({"Id": [1, 2, 3], "Text": ["a", "b", "c"]}).to_csv(raw_dir / "in.csv", index=False)
        return SimpleNamespace(processed=processed_dir)

    def use_client(self, monkeypatch, client):
        monkeypatch.setattr(label_reviews, "Groq", lambda api_key: client)
        return client

    def test_missing_api_key_is_a_config_error(self, workspace, monkeypatch):
        monkeypatch.delenv("GROQ_API_KEY", raising=False)
        with pytest.raises(ConfigError):
            label_reviews.main("in.csv", "Text", 2, 10)

    def test_missing_input_file_is_reported(self, workspace, monkeypatch):
        self.use_client(monkeypatch, FakeClient([]))
        with pytest.raises(DataNotFoundError):
            label_reviews.main("nope.csv", "Text", 2, 10)

    def test_labels_every_row_in_batches_and_checkpoints(self, workspace, monkeypatch):
        client = self.use_client(monkeypatch, FakeClient([
            json.dumps([good(1), good(2)]),
            json.dumps([good(1, "positive", "taste", 0)]),
        ]))
        label_reviews.main("in.csv", "Text", 2, 10)

        saved = pd.read_csv(constants.LABELED_REVIEWS_PATH)
        assert len(saved) == 3
        assert set(saved[constants.LABEL_STATUS_COLUMN]) == {constants.LABEL_STATUS_OK}
        assert saved["sentiment"].tolist() == ["negative", "negative", "positive"]
        assert client.calls == 2
        assert label_reviews.load_checkpoint() == 3

    def test_stops_when_the_daily_budget_is_used_up(self, workspace, monkeypatch):
        client = self.use_client(monkeypatch, FakeClient([json.dumps([good(1), good(2)])]))
        label_reviews.main("in.csv", "Text", 2, 1)  # budget of one request
        assert client.calls == 1
        assert len(pd.read_csv(constants.LABELED_REVIEWS_PATH)) == 2
        assert label_reviews.load_checkpoint() == 2

    def test_rerun_with_everything_done_does_nothing(self, workspace, monkeypatch):
        client = self.use_client(monkeypatch, FakeClient([]))
        workspace.processed.mkdir(parents=True, exist_ok=True)
        label_reviews.save_checkpoint(3)
        label_reviews.main("in.csv", "Text", 2, 10)
        assert client.calls == 0
        assert not constants.LABELED_REVIEWS_PATH.exists()

    def test_failed_batches_are_saved_with_fallback_status(self, workspace, monkeypatch):
        self.use_client(monkeypatch, FakeClient(["bad"] * constants.LABEL_MAX_RETRIES))
        label_reviews.main("in.csv", "Text", 2, 1)
        saved = pd.read_csv(constants.LABELED_REVIEWS_PATH)
        assert set(saved[constants.LABEL_STATUS_COLUMN]) == {constants.LABEL_STATUS_FALLBACK}
        assert set(saved["sentiment"]) == {"neutral"}
