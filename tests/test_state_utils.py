"""Tests for resume-state/scripts/state_utils.py"""

import sys
from pathlib import Path

import pytest

# Add the state_utils module to path
sys.path.insert(0, str(Path(__file__).parent.parent / "resume-state" / "scripts"))

from state_utils import get_next_version_id, now_iso, parse_version_id


class TestParseVersionId:
    """Tests for parse_version_id()"""

    def test_valid_v1(self):
        assert parse_version_id("v1") == 1

    def test_valid_v10(self):
        assert parse_version_id("v10") == 10

    def test_valid_v999(self):
        assert parse_version_id("v999") == 999

    def test_invalid_no_prefix(self):
        with pytest.raises(ValueError, match="Invalid version ID format"):
            parse_version_id("1")

    def test_invalid_uppercase(self):
        with pytest.raises(ValueError, match="Invalid version ID format"):
            parse_version_id("V1")

    def test_invalid_version_word(self):
        with pytest.raises(ValueError, match="Invalid version ID format"):
            parse_version_id("version1")

    def test_invalid_empty(self):
        with pytest.raises(ValueError, match="Invalid version ID format"):
            parse_version_id("")

    def test_invalid_v_only(self):
        with pytest.raises(ValueError, match="Invalid version ID format"):
            parse_version_id("v")


class TestNowIso:
    """Tests for now_iso()"""

    def test_returns_string(self):
        result = now_iso()
        assert isinstance(result, str)

    def test_iso_format(self):
        result = now_iso()
        # ISO format includes T separator and timezone info
        assert "T" in result
        # Should end with +00:00 for UTC
        assert result.endswith("+00:00")

    def test_parseable(self):
        from datetime import datetime

        result = now_iso()
        # Should be parseable as ISO format
        parsed = datetime.fromisoformat(result)
        assert parsed is not None


class TestGetNextVersionId:
    """Tests for get_next_version_id()"""

    def test_empty_versions(self):
        state = {"versions": []}
        assert get_next_version_id(state) == "v1"

    def test_no_versions_key(self):
        state = {}
        assert get_next_version_id(state) == "v1"

    def test_increment_from_v1(self):
        state = {"versions": [{"id": "v1"}]}
        assert get_next_version_id(state) == "v2"

    def test_increment_from_v5(self):
        state = {"versions": [{"id": "v1"}, {"id": "v2"}, {"id": "v5"}]}
        assert get_next_version_id(state) == "v6"

    def test_finds_max_not_last(self):
        # Ensure it finds the max, not just the last entry
        state = {"versions": [{"id": "v10"}, {"id": "v2"}, {"id": "v5"}]}
        assert get_next_version_id(state) == "v11"
