from solution import is_palindrome


def test_sentence():
    assert is_palindrome("A man, a plan, a canal: Panama") is True


def test_not_palindrome():
    assert is_palindrome("hello") is False


def test_empty_and_no_letters():
    assert is_palindrome("") is True
    assert is_palindrome("1 2 !") is True


def test_case():
    assert is_palindrome("Abba") is True


def test_digits_are_ignored():
    assert is_palindrome("ab2a") is True
