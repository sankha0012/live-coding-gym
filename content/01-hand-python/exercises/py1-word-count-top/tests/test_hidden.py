from solution import word_count_top


def test_basic():
    assert word_count_top("a b a c a b", 2) == [("a", 3), ("b", 2)]


def test_lowercases():
    assert word_count_top("The the THE cat", 1) == [("the", 3)]


def test_ties_alphabetical():
    # "pear" appears first in the text, but "apple" wins the tie.
    assert word_count_top("pear apple pear apple kiwi", 3) == [("apple", 2), ("pear", 2), ("kiwi", 1)]


def test_n_larger_than_distinct():
    assert word_count_top("x y", 5) == [("x", 1), ("y", 1)]


def test_empty():
    assert word_count_top("", 3) == []


def test_punctuation_is_not_stripped():
    assert word_count_top("hi hi, hi", 3) == [("hi", 2), ("hi,", 1)]


def test_splits_on_any_whitespace():
    assert word_count_top("a\nb\ta  a", 2) == [("a", 3), ("b", 1)]
