from solution import unique


def test_basic():
    assert unique([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_empty():
    assert unique([]) == []


def test_strings_and_order():
    assert unique(["b", "a", "b", "c", "a"]) == ["b", "a", "c"]


def test_already_unique():
    assert unique([1, 2, 3]) == [1, 2, 3]
