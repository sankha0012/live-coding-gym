import pytest
from solution import chunk


def test_remainder():
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_exact_multiple():
    assert chunk([1, 2, 3, 4, 5, 6], 3) == [[1, 2, 3], [4, 5, 6]]


def test_smaller_than_size():
    assert chunk([1, 2], 5) == [[1, 2]]


def test_empty():
    assert chunk([], 3) == []


def test_bad_size():
    with pytest.raises(ValueError):
        chunk([1, 2], 0)
    with pytest.raises(ValueError):
        chunk([1, 2], -1)


def test_input_unchanged():
    data = [1, 2, 3]
    chunk(data, 2)
    assert data == [1, 2, 3]


def test_bad_size_raises_even_for_empty_input():
    with pytest.raises(ValueError):
        chunk([], 0)
    with pytest.raises(ValueError):
        chunk([], -2)


def test_size_one_and_exact_size():
    assert chunk([1, 2, 3], 1) == [[1], [2], [3]]
    assert chunk([1, 2, 3], 3) == [[1, 2, 3]]
