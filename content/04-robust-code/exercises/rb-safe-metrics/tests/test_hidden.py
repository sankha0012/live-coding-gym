import math

from solution import safe_mean, safe_rate


def test_mean_basic():
    assert safe_mean([1, 2, 3]) == 2


def test_mean_skips_none_and_nan():
    assert safe_mean([1.0, None, float("nan"), 3.0]) == 2.0


def test_mean_keeps_zeros():
    assert safe_mean([0, 0, 6]) == 2.0


def test_mean_empty_and_all_invalid():
    assert safe_mean([]) is None
    assert safe_mean([None, float("nan")]) is None


def test_mean_never_returns_nan():
    r = safe_mean([float("nan"), 1.0])
    assert r == 1.0 and not math.isnan(r)


def test_rate_basic():
    assert safe_rate(1, 4) == 0.25
    assert safe_rate(0, 5) == 0.0


def test_rate_zero_or_negative_total():
    assert safe_rate(3, 0) is None
    assert safe_rate(3, -2) is None


def test_rate_missing_values():
    assert safe_rate(None, 5) is None
    assert safe_rate(2, None) is None
    assert safe_rate(float("nan"), 5) is None
    assert safe_rate(2, float("nan")) is None
