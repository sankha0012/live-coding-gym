from solution import two_sum


def test_basic():
    assert two_sum([2, 7, 11, 15], 9) == [0, 1]


def test_not_found():
    assert two_sum([1, 2, 3], 10) is None


def test_empty():
    assert two_sum([], 5) is None


def test_same_position_not_twice():
    assert two_sum([3, 5], 6) is None


def test_duplicates_and_negatives():
    assert two_sum([3, 3], 6) == [0, 1]
    assert two_sum([-1, 4, 1], 0) == [0, 2]


def test_smallest_j():
    assert two_sum([1, 4, 5, 6], 10) == [1, 3]
    assert two_sum([1, 9, 5, 5], 10) == [0, 1]


def test_smallest_j_beats_smallest_i():
    assert two_sum([5, 1, 9, 5], 10) == [1, 2]


def test_tie_uses_largest_i():
    assert two_sum([2, 2, 8], 10) == [1, 2]
