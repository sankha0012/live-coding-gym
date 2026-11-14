from solution import merge_sorted


def test_interleaves():
    a = [(1, "a"), (4, "a")]
    b = [(2, "b"), (3, "b")]
    assert merge_sorted(a, b) == [(1, "a"), (2, "b"), (3, "b"), (4, "a")]


def test_equal_keys_take_a_first():
    a = [(1, "z")]
    b = [(1, "a")]
    assert merge_sorted(a, b) == [(1, "z"), (1, "a")]


def test_leftover_from_either_list():
    assert merge_sorted([(1, "a")], [(2, "b"), (3, "c")]) == [(1, "a"), (2, "b"), (3, "c")]
    assert merge_sorted([(5, "a"), (6, "b")], [(1, "c")]) == [(1, "c"), (5, "a"), (6, "b")]


def test_empty_lists():
    assert merge_sorted([], []) == []
    assert merge_sorted([(1, "a")], []) == [(1, "a")]
    assert merge_sorted([], [(1, "b")]) == [(1, "b")]


def test_inputs_not_modified():
    a = [(1, "a"), (3, "a")]
    b = [(2, "b")]
    merge_sorted(a, b)
    assert a == [(1, "a"), (3, "a")]
    assert b == [(2, "b")]
