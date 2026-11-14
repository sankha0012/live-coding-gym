from solution import first_unique


def test_basic():
    assert first_unique("leetcode") == 0
    assert first_unique("loveleetcode") == 2


def test_none():
    assert first_unique("aabb") == -1


def test_empty():
    assert first_unique("") == -1


def test_single():
    assert first_unique("z") == 0


def test_case_matters():
    assert first_unique("aA") == 0


def test_unique_after_repeats():
    assert first_unique("aabc") == 2
    assert first_unique("aabcc") == 2
