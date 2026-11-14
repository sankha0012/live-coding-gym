from solution import top_k


def make():
    return [("a", 1), ("b", 5), ("c", 3)]


def test_highest_first():
    assert top_k(make(), 2) == [("b", 5), ("c", 3)]


def test_ties_keep_input_order():
    pairs = [("z", 2), ("a", 2), ("m", 9), ("b", 2)]
    assert top_k(pairs, 3) == [("m", 9), ("z", 2), ("a", 2)]


def test_k_larger_than_list():
    assert top_k(make(), 10) == [("b", 5), ("c", 3), ("a", 1)]


def test_k_zero_and_negative():
    assert top_k(make(), 0) == []
    assert top_k(make(), -1) == []


def test_empty_input():
    assert top_k([], 3) == []


def test_input_not_modified():
    pairs = make()
    top_k(pairs, 2)
    assert pairs == make()
