from solution import batch_split
import pytest


def test_last_batch_short():
    assert batch_split([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_exact_multiple_has_no_empty_batch():
    assert batch_split([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_batch_larger_than_list():
    assert batch_split([1, 2], 5) == [[1, 2]]


def test_empty_list():
    assert batch_split([], 3) == []


def test_invalid_size_raises():
    for n in (0, -1):
        with pytest.raises(ValueError):
            batch_split([1, 2, 3], n)


def test_input_not_modified():
    items = [1, 2, 3]
    batch_split(items, 2)
    assert items == [1, 2, 3]
