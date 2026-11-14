from solution import first_index


def test_basic():
    assert first_index([1, 3, 5, 7, 9], 7) == 3


def test_duplicates_first():
    assert first_index([1, 2, 2, 2, 3], 2) == 1
    assert first_index([5, 5, 5, 5], 5) == 0
    assert first_index([1, 2, 2, 3], 2) == 1
    assert first_index([1, 1, 2, 2, 2, 2, 2], 2) == 2


def test_missing():
    assert first_index([1, 3, 5], 4) == -1
    assert first_index([1, 3, 5], 0) == -1
    assert first_index([1, 3, 5], 9) == -1


def test_empty_and_single():
    assert first_index([], 1) == -1
    assert first_index([4], 4) == 0
    assert first_index([4], 5) == -1


def test_ends():
    assert first_index([1, 2, 3, 4], 1) == 0
    assert first_index([1, 2, 3, 4], 4) == 3
