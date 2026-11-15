from solution import compress_spaces


def test_basic():
    assert compress_spaces("  a   b  ") == "a b"


def test_already_clean():
    assert compress_spaces("a b c") == "a b c"


def test_only_spaces_and_empty():
    assert compress_spaces("     ") == ""
    assert compress_spaces("") == ""


def test_other_whitespace_kept():
    assert compress_spaces("a\tb  c") == "a\tb c"


def test_long_runs():
    assert compress_spaces("a     b") == "a b"


def test_only_spaces_are_trimmed_at_the_edges():
    assert compress_spaces(" \ta  b\n ") == "\ta b\n"
    assert compress_spaces("a \t b") == "a \t b"
