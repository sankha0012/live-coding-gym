from solution import safe_int


def test_strings():
    assert safe_int("42") == 42
    assert safe_int("  7 ") == 7


def test_int_passes_through():
    assert safe_int(5) == 5
    assert safe_int(-5) == -5
    assert safe_int("-12") == -12


def test_bad_text_gives_default():
    assert safe_int("abc") == 0
    assert safe_int("", default=-1) == -1
    assert safe_int("7.0", default=9) == 9


def test_none_gives_default():
    assert safe_int(None) == 0
    assert safe_int(None, default=3) == 3


def test_floats():
    assert safe_int(7.0) == 7
    assert safe_int(7.5, default=-1) == -1
    assert safe_int(float("nan"), default=-1) == -1
    assert safe_int(float("inf"), default=-1) == -1
