from solution import guard_scores


def test_range_example():
    assert guard_scores([0.2, 1.5, -0.1, 1.0], lo=0.0, hi=1.0) == ([0.2, 0.5, 0.5, 1.0], 2)


def test_only_hi():
    assert guard_scores([-3, 9], hi=5) == ([-3, 0.5], 1)


def test_only_lo():
    assert guard_scores([-3, 9], lo=0) == ([0.5, 9], 1)


def test_bounds_are_inclusive():
    assert guard_scores([0, 1], lo=0, hi=1) == ([0, 1], 0)


def test_custom_fallback_with_bounds_and_nan():
    got = guard_scores([2.0, float("nan"), 0.4, None], fallback=0.0, lo=0, hi=1)
    assert got == ([0.0, 0.0, 0.4, 0.0], 3)


def test_no_bounds_unchanged():
    assert guard_scores([-0.5, 2.0]) == ([-0.5, 2.0], 0)
