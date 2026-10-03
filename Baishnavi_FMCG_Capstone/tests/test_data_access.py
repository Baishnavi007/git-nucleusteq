"""Tests for the shared date filtering rule (repositories/data_access.py)."""

import pytest

from src.exceptions import DataNotFoundError, InvalidInputError
from src.repositories.data_access import filter_by_date, get_dataset_today, load_reviews


def test_load_reviews_returns_all_synthetic_rows(synthetic_reviews_env):
    df = load_reviews()
    assert len(df) == 5


def _write_labelled_csv(tmp_path, monkeypatch, statuses):
    import pandas as pd
    from src.repositories import data_access
    rows = [
        (i + 1, f"P{i}", f"Product {i}", "U", 3, 1_356_998_400 + i * 86_400, "s", "t",
         "positive", "taste", 0, status)
        for i, status in enumerate(statuses)
    ]
    columns = ["Id", "ProductId", "ProductName", "UserId", "Score", "Time", "Summary", "Text",
               "sentiment", "aspect", "severity", "label_status"]
    csv_path = tmp_path / "scrubbed_reviews.csv"
    pd.DataFrame(rows, columns=columns).to_csv(csv_path, index=False)
    monkeypatch.setattr(data_access.constants, "SCRUBBED_REVIEWS_PATH", csv_path)
    data_access.reset_caches_for_tests()


def test_fallback_and_unverified_rows_are_excluded(tmp_path, monkeypatch):
    from src.repositories import data_access
    _write_labelled_csv(tmp_path, monkeypatch, ["ok", "fallback", "unverified", "ok"])
    assert load_reviews()["Id"].tolist() == [1, 4]
    data_access.reset_caches_for_tests()


def test_all_rows_unverified_raises_data_not_found(tmp_path, monkeypatch):
    from src.repositories import data_access
    _write_labelled_csv(tmp_path, monkeypatch, ["fallback", "unverified"])
    with pytest.raises(DataNotFoundError):
        load_reviews()
    data_access.reset_caches_for_tests()


def test_missing_file_raises_data_not_found(tmp_path, monkeypatch):
    from src.repositories import data_access
    monkeypatch.setattr(data_access.constants, "SCRUBBED_REVIEWS_PATH", tmp_path / "missing.csv")
    data_access.reset_caches_for_tests()
    with pytest.raises(DataNotFoundError):
        load_reviews()


def test_end_date_is_inclusive_of_the_whole_day(synthetic_reviews_env):
    # Row 1 is on 2013-01-01 (epoch 1356998400). A naive `<= end_date`
    # comparison (midnight) would wrongly exclude it -- this is the bug
    # that used to drop the last day of every range.
    df = load_reviews()
    filtered = filter_by_date(df, start_date="2013-01-01", end_date="2013-01-01")
    assert len(filtered) == 1
    assert filtered.iloc[0]["Id"] == 1


def test_date_range_filters_correctly(synthetic_reviews_env):
    df = load_reviews()
    filtered = filter_by_date(df, start_date="2013-01-01", end_date="2013-01-03")
    assert set(filtered["Id"]) == {1, 2, 3}


def test_invalid_date_raises_invalid_input(synthetic_reviews_env):
    df = load_reviews()
    with pytest.raises(InvalidInputError):
        filter_by_date(df, start_date="not-a-date", end_date=None)


def test_dataset_today_is_the_max_review_date(synthetic_reviews_env):
    assert get_dataset_today().isoformat() == "2013-01-05"
