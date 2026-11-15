import pytest
from solution import latest_version

RECORDS = [
    {"name": "eta", "version": "1.9.0", "stage": "production"},
    {"name": "eta", "version": "1.10.0", "stage": "production"},
    {"name": "eta", "version": "2.0.0", "stage": "production"},
    {"name": "eta", "version": "2.0.1", "stage": "staging"},
    {"name": "eta", "version": "v3", "stage": "production"},
]


def test_cap_picks_highest_not_above():
    assert latest_version(RECORDS, "eta", "production", "1.10")["version"] == "1.10.0"
    assert latest_version(RECORDS, "eta", "production", "1.9.5")["version"] == "1.9.0"


def test_equal_to_cap_is_allowed_with_padding():
    assert latest_version(RECORDS, "eta", "production", "2")["version"] == "2.0.0"
    assert latest_version(RECORDS, "eta", "production", "2.0.0.0")["version"] == "2.0.0"


def test_cap_applies_within_stage_only():
    assert latest_version(RECORDS, "eta", "staging", "3.0")["version"] == "2.0.1"
    with pytest.raises(LookupError):
        latest_version(RECORDS, "eta", "staging", "2.0")


def test_nothing_under_cap_raises():
    with pytest.raises(LookupError):
        latest_version(RECORDS, "eta", "production", "1.0")


def test_cap_returns_original_record():
    assert latest_version(RECORDS, "eta", "production", "1.9.9") is RECORDS[0]
