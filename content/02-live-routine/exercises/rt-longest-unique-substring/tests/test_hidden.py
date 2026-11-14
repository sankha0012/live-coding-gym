from solution import longest_unique


def test_basic():
    assert longest_unique("abcabcbb") == 3


def test_all_same():
    assert longest_unique("bbbbb") == 1


def test_empty():
    assert longest_unique("") == 0


def test_window_must_not_move_back():
    assert longest_unique("abba") == 2


def test_whole_string_unique():
    assert longest_unique("abcdef") == 6


def test_case_matters():
    assert longest_unique("aA") == 2


def test_keeps_overlap_after_repeat():
    assert longest_unique("abcdbefg") == 6
