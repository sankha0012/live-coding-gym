import pytest

from solution import clamp


def test_inside_range_unchanged():
    assert clamp(5, 0, 10) == 5


def test_below_lower_bound():
    assert clamp(-3, 0, 10) == 0


def test_above_upper_bound():
    assert clamp(42, 0, 10) == 10


def test_equal_bounds_allowed():
    assert clamp(5, 5, 5) == 5
    assert clamp(9, 5, 5) == 5


def test_negative_and_float_values():
    assert clamp(-2.5, -5, -1) == -2.5
    assert clamp(-9.5, -5, -1) == -5


def test_inverted_bounds_raise():
    with pytest.raises(ValueError):
        clamp(5, 10, 0)
