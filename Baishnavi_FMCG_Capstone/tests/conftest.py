"""
conftest.py
====================
Shared pytest fixtures. `synthetic_reviews_env` builds a small, fully
synthetic scrubbed_reviews.csv (no real data, no network, no API keys) so
the tests exercise the actual filtering/aggregation code paths.
"""

import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.repositories import data_access


@pytest.fixture
def synthetic_reviews_env(tmp_path, monkeypatch):
    rows = [
        # Id, ProductId, ProductName, UserId, Score, Time (epoch s), Summary, Text,
        # HelpfulnessNumerator, HelpfulnessDenominator, sentiment, aspect, severity
        (1, "P1", "Chicken Formula", "U1", 5, 1_356_998_400, "Great!", "My dog loves it.", 2, 2, "positive", "taste", 0),
        (2, "P1", "Chicken Formula", "U2", 1, 1_357_084_800, "Bad smell", "Package arrived with a weird smell.", 0, 1, "negative", "other", 3),
        (3, "P2", "Beef Formula", "U3", 2, 1_357_171_200, "Leaky bag", "The bag arrived torn and leaking.", 1, 3, "negative", "packaging", 2),
        (4, "P2", "Beef Formula", "U4", 4, 1_357_257_600, "Good value", "Price is fair for the size.", 3, 3, "positive", "price", 0),
        (5, "P3", "Salmon Formula", "U5", 1, 1_357_344_000, "Contamination", "Found mold inside, made my cat sick.", 5, 5, "negative", "other", 5),
    ]
    columns = ["Id", "ProductId", "ProductName", "UserId", "Score", "Time", "Summary", "Text",
              "HelpfulnessNumerator", "HelpfulnessDenominator", "sentiment", "aspect", "severity"]
    df = pd.DataFrame(rows, columns=columns)

    processed_dir = tmp_path / "processed"
    processed_dir.mkdir()
    csv_path = processed_dir / "scrubbed_reviews.csv"
    df.to_csv(csv_path, index=False)

    monkeypatch.setattr(data_access.constants, "SCRUBBED_REVIEWS_PATH", csv_path)
    data_access.reset_caches_for_tests()
    yield
    data_access.reset_caches_for_tests()
