from solution import top_k


def test_basic():
    assert top_k([1, 1, 1, 2, 2, 3], 2) == [1, 2]


def test_ties_by_first_appearance():
    assert top_k(["b", "a", "b", "c", "a", "d"], 2) == ["b", "a"]


def test_ties_all_equal():
    assert top_k(["x", "y", "z"], 3) == ["x", "y", "z"]


def test_k_too_big():
    assert top_k([1, 2, 2], 10) == [2, 1]


def test_empty_and_zero():
    assert top_k([], 3) == []
    assert top_k([1, 1], 0) == []


def test_ties_first_appearance_not_last():
    assert top_k(["a", "b", "b", "a"], 2) == ["a", "b"]
    assert top_k(["c", "a", "b", "a", "b"], 2) == ["a", "b"]
    assert top_k(["a", "b", "c", "c", "b", "a", "d"], 4) == ["a", "b", "c", "d"]
