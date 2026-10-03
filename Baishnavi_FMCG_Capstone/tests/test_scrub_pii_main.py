"""End-to-end test of scrub_pii.main(): reads a small labeled CSV from a
temp folder and checks what lands in the scrubbed file and the policy note.
"""

import pandas as pd
import pytest

from src.config import constants
from src.exceptions import DataNotFoundError
from src.rag import scrub_pii


@pytest.fixture
def pii_paths(tmp_path, monkeypatch):
    processed = tmp_path / "processed"
    processed.mkdir()
    docs = tmp_path / "docs"
    monkeypatch.setattr(constants, "PROCESSED_DIR", processed)
    monkeypatch.setattr(constants, "DOCS_DIR", docs)
    monkeypatch.setattr(constants, "LABELED_REVIEWS_PATH", processed / "labeled.csv")
    monkeypatch.setattr(constants, "SCRUBBED_REVIEWS_PATH", processed / "scrubbed.csv")
    monkeypatch.setattr(constants, "PII_POLICY_PATH", docs / "pii_policy.md")
    return tmp_path


def write_labeled(rows):
    pd.DataFrame(rows).to_csv(constants.LABELED_REVIEWS_PATH, index=False)


class TestMain:
    def test_missing_labeled_file_is_reported(self, pii_paths):
        with pytest.raises(DataNotFoundError):
            scrub_pii.main()

    def test_masks_identity_columns_and_cleans_free_text(self, pii_paths):
        write_labeled([{
            "Id": 1, "ProfileName": "Jane Doe", "UserId": "U1",
            "Summary": "<b>Great</b> stuff",
            "Text": "Loved it, email me at jane@example.com &amp; thanks",
        }])
        scrub_pii.main()

        saved = pd.read_csv(constants.SCRUBBED_REVIEWS_PATH)
        assert saved.loc[0, "ProfileName"] == constants.PII_MASK_TOKEN
        assert saved.loc[0, "UserId"] == "U1"  # opaque ID is deliberately kept
        assert "<b>" not in saved.loc[0, "Summary"]
        assert "jane@example.com" not in saved.loc[0, "Text"]
        assert "&amp;" not in saved.loc[0, "Text"]

    def test_missing_identity_values_stay_missing(self, pii_paths):
        write_labeled([{"Id": 1, "ProfileName": None, "Summary": "ok", "Text": "fine"}])
        scrub_pii.main()
        assert pd.isna(pd.read_csv(constants.SCRUBBED_REVIEWS_PATH).loc[0, "ProfileName"])

    def test_writes_the_policy_note_with_the_row_count(self, pii_paths):
        write_labeled([
            {"Id": 1, "Summary": "a", "Text": "b"},
            {"Id": 2, "Summary": "c", "Text": "d"},
        ])
        scrub_pii.main()
        note = constants.PII_POLICY_PATH.read_text(encoding="utf-8")
        assert note == scrub_pii.build_policy_note(2)
