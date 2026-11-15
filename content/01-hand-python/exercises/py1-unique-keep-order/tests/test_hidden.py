from solution import unique


def test_basic():
    assert unique([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_empty():
    assert unique([]) == []


def test_strings_and_order():
    assert unique(["b", "a", "b", "c", "a"]) == ["b", "a", "c"]


def test_already_unique():
    assert unique([1, 2, 3]) == [1, 2, 3]


def test_falsy_items_are_kept():
    assert unique([0, "", 0, None, ""]) == [0, "", None]
    assert unique([1, 0, 1]) == [1, 0]
