import pytest
from solution import latest_version

RECORDS = [
    {"name": "eta", "version": "1.9.0", "stage": "production"},
    {"name": "eta", "version": "1.10.0", "stage": "production"},
    {"name": "eta", "version": "2.0.0", "stage": "staging"},
    {"name": "fraud", "version": "3.0.0", "stage": "production"},
]


def test_semantic_not_string_order():
    assert latest_version(RECORDS, "eta", "production") is RECORDS[1]


def test_filters_by_name_and_stage():
    assert latest_version(RECORDS, "eta", "staging") is RECORDS[2]
    assert latest_version(RECORDS, "fraud", "production") is RECORDS[3]


def test_not_found_raises_lookup_error():
    with pytest.raises(LookupError):
        latest_version(RECORDS, "eta", "archived")
    with pytest.raises(LookupError):
        latest_version(RECORDS, "nope", "production")
    with pytest.raises(LookupError):
        latest_version([], "eta", "production")


def test_padding_tie_and_bad_versions():
    recs = [
        {"name": "m", "version": "2.1", "stage": "p"},
        {"name": "m", "version": "2.1.0", "stage": "p"},
        {"name": "m", "version": "2.0.9", "stage": "p"},
        {"name": "m", "version": "v3", "stage": "p"},
        {"name": "m", "version": "", "stage": "p"},
    ]
    assert latest_version(recs, "m", "p") is recs[0]


def test_only_bad_versions_raises():
    with pytest.raises(LookupError):
        latest_version([{"name": "m", "version": "abc", "stage": "p"}], "m", "p")


def test_four_part_versions():
    recs = [
        {"name": "m", "version": "1.2.3.4", "stage": "p"},
        {"name": "m", "version": "1.2.3.10", "stage": "p"},
    ]
    assert latest_version(recs, "m", "p") is recs[1]


def test_trailing_zeros_and_long_versions():
    recs = [
        {"name": "m", "version": "1", "stage": "p"},
        {"name": "m", "version": "1.0.0.0.0.0.0.0.0.1", "stage": "p"},
        {"name": "m", "version": "1.0.0.0.0.0.0.0.0.0.0", "stage": "p"},
    ]
    assert latest_version(recs, "m", "p") is recs[1]
    tie = [{"name": "m", "version": "1.0", "stage": "p"}, {"name": "m", "version": "1", "stage": "p"}]
    assert latest_version(tie, "m", "p") is tie[0]
