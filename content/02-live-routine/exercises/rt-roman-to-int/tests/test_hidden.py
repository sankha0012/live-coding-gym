from solution import roman_to_int


def test_simple():
    assert roman_to_int("III") == 3
    assert roman_to_int("LVIII") == 58


def test_subtractive():
    assert roman_to_int("IV") == 4
    assert roman_to_int("IX") == 9
    assert roman_to_int("XL") == 40
    assert roman_to_int("CM") == 900


def test_long():
    assert roman_to_int("MCMXCIV") == 1994
    assert roman_to_int("MMMCMXCIX") == 3999


def test_empty():
    assert roman_to_int("") == 0
