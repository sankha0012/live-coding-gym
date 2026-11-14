from solution import anagram_groups


def test_basic():
    got = anagram_groups(["tea", "eat", "tan", "ate", "nat", "bat"])
    assert got == [["bat"], ["tan", "nat"], ["tea", "eat", "ate"]]


def test_empty():
    assert anagram_groups([]) == []


def test_single_and_empty_word():
    assert anagram_groups(["a"]) == [["a"]]
    assert anagram_groups(["", ""]) == [["", ""]]


def test_duplicates_kept():
    assert anagram_groups(["ab", "ba", "ab"]) == [["ab", "ba", "ab"]]


def test_sorted_by_first_word_not_by_key():
    assert anagram_groups(["zy", "abc", "yz", "cab"]) == [["abc", "cab"], ["zy", "yz"]]
