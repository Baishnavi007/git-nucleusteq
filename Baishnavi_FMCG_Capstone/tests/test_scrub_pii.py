"""Tests for the PII-scrubbing helpers in src/rag/scrub_pii.py -- all pure
functions, so these run with no file I/O, no network, and no fixtures."""

import pandas as pd

from src.rag.scrub_pii import build_policy_note, clean_html, mask_value, redact_contact_info


class TestCleanHtml:
    def test_strips_tags(self):
        assert clean_html("<b>Great</b> product") == "Great product"

    def test_unescapes_entities(self):
        assert clean_html("Tom &amp; Jerry&#39;s food") == "Tom & Jerry's food"

    def test_collapses_whitespace(self):
        assert clean_html("Too   much\n\nspace") == "Too much space"

    def test_passes_through_missing_value(self):
        assert pd.isna(clean_html(float("nan")))

    def test_plain_text_is_unchanged(self):
        assert clean_html("Nothing to clean here.") == "Nothing to clean here."


class TestRedactContactInfo:
    def test_redacts_email(self):
        result = redact_contact_info("Contact me at jane.doe@example.com please")
        assert "jane.doe@example.com" not in result
        assert "[email redacted]" in result

    def test_redacts_phone(self):
        result = redact_contact_info("Call me at 555-123-4567")
        assert "555-123-4567" not in result
        assert "[phone redacted]" in result

    def test_leaves_normal_text_untouched(self):
        text = "Great taste, will buy again."
        assert redact_contact_info(text) == text

    def test_passes_through_missing_value(self):
        assert pd.isna(redact_contact_info(float("nan")))


class TestMaskValue:
    def test_masks_a_real_value(self):
        assert mask_value("Jane D.") == "******"

    def test_leaves_missing_value_as_missing(self):
        assert pd.isna(mask_value(float("nan")))


class TestBuildPolicyNote:
    def test_includes_the_row_count(self):
        note = build_policy_note(1234)
        assert "1234 labeled reviews" in note

    def test_includes_the_mask_token(self):
        from src.config import constants
        note = build_policy_note(1)
        assert constants.PII_MASK_TOKEN in note

    def test_is_nonempty_markdown(self):
        note = build_policy_note(0)
        assert note.startswith("# ")
