from solution import pairs


def test_basic():
    assert pairs([1, 2, 3, 4]) == [(1, 2), (2, 3), (3, 4)]


def test_empty():
    assert pairs([]) == []


def test_single():
    assert pairs([1]) == []


def test_two():
    assert pairs(["a", "b"]) == [("a", "b")]


def test_returns_tuples():
    assert all(isinstance(p, tuple) for p in pairs([1, 2, 3]))


def test_duplicates_kept():
    assert pairs([1, 1, 2, 1]) == [(1, 1), (1, 2), (2, 1)]
