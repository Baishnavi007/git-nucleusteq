"""Tests for the shared date filtering rule (repositories/data_access.py)."""

import pytest

from src.exceptions import DataNotFoundError, InvalidInputError
from src.repositories.data_access import filter_by_date, get_dataset_today, load_reviews


def test_load_reviews_returns_all_synthetic_rows(synthetic_reviews_env):
    df = load_reviews()
    assert len(df) == 5


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
