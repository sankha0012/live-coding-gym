from solution import merge_intervals


def test_gap_merges_near_intervals():
    assert merge_intervals([[1, 2], [4, 5]], gap=2) == [[1, 5]]


def test_gap_too_small():
    assert merge_intervals([[1, 2], [4, 5]], gap=1) == [[1, 2], [4, 5]]


def test_gap_chain_unsorted():
    assert merge_intervals([[7, 8], [1, 2], [4, 5]], gap=2) == [[1, 8]]


def test_gap_mixed():
    assert merge_intervals([[1, 2], [4, 5], [20, 21]], gap=3) == [[1, 5], [20, 21]]


def test_gap_zero_and_default_unchanged():
    assert merge_intervals([[1, 2], [4, 5]]) == [[1, 2], [4, 5]]
    assert merge_intervals([[1, 2], [2, 3]], gap=0) == [[1, 3]]


def test_gap_input_not_changed():
    data = [[4, 5], [1, 2]]
    merge_intervals(data, gap=2)
    assert data == [[4, 5], [1, 2]]
