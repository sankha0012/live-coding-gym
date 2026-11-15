from solution import merge_intervals


def test_basic():
    assert merge_intervals([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]


def test_unsorted():
    assert merge_intervals([[8, 10], [1, 3], [2, 6]]) == [[1, 6], [8, 10]]


def test_touching():
    assert merge_intervals([[1, 2], [2, 3]]) == [[1, 3]]


def test_contained():
    assert merge_intervals([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]


def test_empty_and_single():
    assert merge_intervals([]) == []
    assert merge_intervals([[5, 6]]) == [[5, 6]]


def test_input_not_changed():
    data = [[3, 4], [1, 3]]
    merge_intervals(data)
    assert data == [[3, 4], [1, 3]]


def test_chain_and_point():
    assert merge_intervals([[5, 7], [1, 3], [3, 5], [9, 9]]) == [[1, 7], [9, 9]]
