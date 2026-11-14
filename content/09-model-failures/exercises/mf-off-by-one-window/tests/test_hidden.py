import pytest

from solution import rolling_mean


def test_basic():
    assert rolling_mean([1, 2, 3, 4], 2) == [None, 1.5, 2.5, 3.5]


def test_includes_current_value():
    assert rolling_mean([10, 20, 30], 3) == [None, None, 20.0]


def test_first_full_window_is_not_skipped():
    out = rolling_mean([2, 4, 6, 8, 10], 3)
    assert out[:2] == [None, None]
    assert out[2] == 4.0
    assert out[4] == 8.0


def test_window_one_is_identity():
    assert rolling_mean([5, 6, 7], 1) == [5.0, 6.0, 7.0]


def test_window_larger_than_input():
    assert rolling_mean([1, 2], 5) == [None, None]


def test_empty():
    assert rolling_mean([], 3) == []


def test_bad_window():
    with pytest.raises(ValueError):
        rolling_mean([1, 2], 0)
