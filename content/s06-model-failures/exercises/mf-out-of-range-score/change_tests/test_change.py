from solution import clip_probs


def test_percent_scale():
    got, n = clip_probs([-5, 40, 120], hi=100)
    assert got == [0.0, 40, 100.0]
    assert n == 2


def test_hi_two_keeps_values_below():
    assert clip_probs([0.5, 1.5], hi=2) == ([0.5, 1.5], 0)


def test_value_equal_to_hi_not_counted():
    assert clip_probs([100, 100.5], hi=100) == ([100, 100.0], 1)


def test_clipped_value_is_float():
    got, _ = clip_probs([9], hi=5)
    assert got == [5.0] and isinstance(got[0], float)


def test_default_still_one():
    assert clip_probs([1.5, -1]) == ([1.0, 0.0], 2)
