from solution import count_vowels


def test_basic():
    assert count_vowels("hello world") == 3


def test_upper():
    assert count_vowels("AEIOU") == 5


def test_none_and_y():
    assert count_vowels("rhythm myth") == 0


def test_empty():
    assert count_vowels("") == 0


def test_repeats_and_mixed_case():
    assert count_vowels("banana") == 3
    assert count_vowels("Education") == 5
