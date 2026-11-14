from solution import group_by_length


def test_basic():
    assert group_by_length(["hi", "yo", "cat"]) == {2: ["hi", "yo"], 3: ["cat"]}


def test_input_order_kept():
    assert group_by_length(["bb", "aa", "cc"]) == {2: ["bb", "aa", "cc"]}


def test_duplicates_kept():
    assert group_by_length(["a", "a", "bb"]) == {1: ["a", "a"], 2: ["bb"]}


def test_empty():
    assert group_by_length([]) == {}


def test_empty_string_has_length_zero():
    assert group_by_length(["", "x"]) == {0: [""], 1: ["x"]}
