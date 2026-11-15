from solution import top_k


def test_filters_rare_items():
    assert top_k(["b", "a", "b", "c", "a", "d"], 5, min_count=2) == ["b", "a"]


def test_k_still_applies():
    assert top_k([1, 1, 2, 2, 3, 3], 2, min_count=2) == [1, 2]


def test_nothing_reaches_min_count():
    assert top_k([1, 2, 3], 3, min_count=2) == []


def test_min_count_three():
    assert top_k([1, 1, 1, 2, 2, 3], 3, min_count=3) == [1]


def test_default_unchanged():
    assert top_k([1, 2, 2], 10) == [2, 1]
    assert top_k([1, 2, 2], 10, min_count=1) == [2, 1]
