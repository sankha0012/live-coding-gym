import pytest

from solution import serve_features, train_features

STATS = {"mean": 2.0, "std": 1.5}


def test_large_amount_is_clipped():
    got = serve_features({"amount": 1000000.0, "category": "x"}, STATS, clip=5)
    assert got["amount_z"] == pytest.approx(5.0)


def test_very_negative_value_is_clipped():
    stats = {"mean": 20.0, "std": 1.0}  # log1p(5) is about 1.79, so z is about -18
    got = serve_features({"amount": 5.0, "category": "x"}, stats, clip=5)
    assert got["amount_z"] == pytest.approx(-5.0)


def test_value_inside_range_is_untouched():
    row = {"amount": 30.0, "category": " Pizza "}
    want = train_features([row], STATS)[0]
    got = serve_features(row, STATS, clip=50)
    assert got["amount_z"] == pytest.approx(want["amount_z"])
    assert got["category"] == "pizza"


def test_clip_none_changes_nothing():
    row = {"amount": 1000000.0, "category": "x"}
    want = train_features([row], STATS)[0]
    assert serve_features(row, STATS, clip=None)["amount_z"] == pytest.approx(want["amount_z"])
    assert serve_features(row, STATS)["amount_z"] == pytest.approx(want["amount_z"])


def test_category_and_keys_unchanged_when_clipping():
    got = serve_features({"amount": 1000000.0, "category": " BIG "}, STATS, clip=1)
    assert got == {"amount_z": pytest.approx(1.0), "category": "big"}
