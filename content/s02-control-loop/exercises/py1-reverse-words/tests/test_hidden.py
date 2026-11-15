from solution import reverse_words


def test_basic():
    assert reverse_words("the sky is blue") == "blue is sky the"


def test_extra_spaces():
    assert reverse_words("  a   b ") == "b a"


def test_empty():
    assert reverse_words("") == ""


def test_single_word():
    assert reverse_words("hi") == "hi"
