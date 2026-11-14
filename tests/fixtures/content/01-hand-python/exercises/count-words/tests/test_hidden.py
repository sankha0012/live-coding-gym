from solution import count_words


def test_basic():
    assert count_words("a b a") == {"a": 2, "b": 1}


def test_mixed_case():
    assert count_words("A a") == {"a": 2}


def test_empty():
    assert count_words("") == {}
