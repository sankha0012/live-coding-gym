from solution import caesar


def test_basic():
    assert caesar("Abc, xyz!", 3) == "Def, abc!"


def test_negative():
    assert caesar("abc", -1) == "zab"


def test_big_shift():
    assert caesar("abc", 29) == "def"


def test_zero_and_empty():
    assert caesar("Hi there", 0) == "Hi there"
    assert caesar("", 5) == ""


def test_keeps_other_chars():
    assert caesar("1 2 !", 4) == "1 2 !"


def test_upper_wrap_and_big_negative():
    assert caesar("XYZ", 3) == "ABC"
    assert caesar("abc", -27) == "zab"


def test_accented_unchanged():
    assert caesar("é", 1) == "é"
