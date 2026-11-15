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


def test_mean_all_zeros_and_negatives_and_fractions():
    assert safe_mean([0, 0]) == 0.0 and safe_mean([0]) == 0.0
    assert safe_mean([0.0, None, 0.0]) == 0.0
    assert safe_mean([-1, -3]) == -2.0
    assert safe_mean([-2, 2, None]) == 0.0
    assert safe_mean([1, 2]) == 1.5
    assert safe_mean([1, 2, 2, None, None]) == 5 / 3


def test_mean_does_not_modify_input():
    vals = [1.0, None, float("nan"), 3.0]
    safe_mean(vals)
    assert len(vals) == 4 and vals[1] is None and math.isnan(vals[2])


def test_rate_small_total_and_values_above_one():
    assert safe_rate(1, 0.5) == 2.0
    assert safe_rate(1, 0.25) == 4.0
    assert safe_rate(5, 4) == 1.25
    assert safe_rate(-1, 4) == -0.25
    assert safe_rate(0, 0.001) == 0.0
    assert safe_rate(3, 0.0) is None
