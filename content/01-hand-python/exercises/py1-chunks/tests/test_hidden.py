import pytest
from solution import chunks


def test_basic():
    assert chunks([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_exact_fit():
    assert chunks([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


def test_empty():
    assert chunks([], 3) == []


def test_n_bigger_than_list():
    assert chunks([1, 2], 5) == [[1, 2]]


@pytest.mark.parametrize("n", [0, -1])
def test_bad_n(n):
    with pytest.raises(ValueError):
        chunks([1, 2, 3], n)


def test_bad_n_with_empty_list():
    with pytest.raises(ValueError):
        chunks([], 0)
