import pytest

from solution import serve_features, train_features

STATS = {"mean": 2.0, "std": 1.5}


def check(row):
    want = train_features([row], STATS)[0]
    got = serve_features(row, STATS)
    assert got["category"] == want["category"]
    assert got["amount_z"] == pytest.approx(want["amount_z"])


def test_plain_row():
    check({"amount": 30.0, "category": "pizza"})


def test_log1p_not_log():
    # log and log1p differ for every amount, and log(0) fails
    check({"amount": 0.0, "category": "pizza"})
    check({"amount": 1.0, "category": "pizza"})


def test_missing_amount():
    check({"amount": None, "category": "pizza"})
    check({"category": "pizza"})


def test_category_is_cleaned():
    check({"amount": 5.0, "category": "  Pizza "})
    assert serve_features({"amount": 5.0, "category": "BURGER"}, STATS)["category"] == "burger"


def test_missing_category():
    check({"amount": 5.0})
    check({"amount": 5.0, "category": None})
    check({"amount": 5.0, "category": ""})


def test_train_reference_unchanged():
    got = train_features([{"amount": 0.0, "category": " A "}], STATS)
    assert got == [{"amount_z": -4.0 / 3.0, "category": "a"}]


def test_whitespace_only_category_matches_training():
    # training strips it to "", it is not a missing category
    check({"amount": 5.0, "category": "   "})
    assert serve_features({"amount": 5.0, "category": "   "}, STATS)["category"] == ""


def test_same_keys_as_training():
    row = {"amount": 3.0, "category": "Pizza", "extra": 1}
    assert set(serve_features(row, STATS)) == set(train_features([row], STATS)[0])
