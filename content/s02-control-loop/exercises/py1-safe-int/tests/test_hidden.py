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


def test_whole_float_becomes_int_type():
    assert type(safe_int(7.0)) is int
    assert type(safe_int(-3.0)) is int
    assert type(safe_int("12")) is int


def test_near_whole_float_is_not_whole():
    assert safe_int(7.0000000001, default=-1) == -1
    assert safe_int(6.9999999999, default=-1) == -1


def test_large_values_are_exact():
    assert safe_int(2**70) == 2**70
    assert safe_int("9007199254740993") == 9007199254740993
