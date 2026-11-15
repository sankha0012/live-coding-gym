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


def _to_roman(n):
    out = ""
    for v, r in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
                 (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= v:
            out += r
            n -= v
    return out


def test_every_subtractive_pair():
    assert roman_to_int("CD") == 400
    assert roman_to_int("XC") == 90
    assert roman_to_int("CDXLIV") == 444
    assert roman_to_int("XLIX") == 49


def test_all_values_1_to_3999():
    for n in range(1, 4000):
        assert roman_to_int(_to_roman(n)) == n, n
