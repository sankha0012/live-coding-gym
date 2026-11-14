import pytest

from solution import moving_average


def test_basic_windows():
    assert moving_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]


def test_window_equals_length_gives_one_mean():
    assert moving_average([2, 4, 6], 3) == [4]


def test_window_larger_than_list_is_empty():
    assert moving_average([1, 2], 5) == []
    assert moving_average([], 3) == []


def test_invalid_window_raises():
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 0)
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], -1)


def test_input_not_modified():
    data = [3, 1, 2]
    assert moving_average(data, 2) == [2, 1.5]
    assert data == [3, 1, 2]
