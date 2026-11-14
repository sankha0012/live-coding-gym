import math

from solution import guard_scores


def test_all_good():
    assert guard_scores([0.1, 0.9, 0]) == ([0.1, 0.9, 0], 0)


def test_nan_inf_none():
    got, n = guard_scores([0.2, float("nan"), None, float("inf"), float("-inf"), 0.7])
    assert got == [0.2, 0.5, 0.5, 0.5, 0.5, 0.7]
    assert n == 4


def test_custom_fallback_and_string():
    assert guard_scores(["x", 0.3], fallback=0.0) == ([0.0, 0.3], 1)


def test_bool_is_bad():
    assert guard_scores([True, 0.4, False]) == ([0.5, 0.4, 0.5], 2)


def test_empty():
    assert guard_scores([]) == ([], 0)


def test_input_not_modified():
    src = [float("nan"), 1.0]
    guard_scores(src)
    assert math.isnan(src[0]) and src[1] == 1.0
