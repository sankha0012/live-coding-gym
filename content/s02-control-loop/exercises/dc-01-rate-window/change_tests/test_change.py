from solution import is_rate_limited


def test_default_still_ignores_request_at_now():
    assert is_rate_limited([95, 100], 100, 10, 2) is False


def test_include_now_counts_request_at_now():
    assert is_rate_limited([95, 100], 100, 10, 2, include_now=True) is True


def test_include_now_keeps_window_start_inclusive():
    assert is_rate_limited([90, 100], 100, 10, 2, include_now=True) is True
    assert is_rate_limited([89, 100], 100, 10, 2, include_now=True) is False


def test_include_now_does_not_count_later_requests():
    # now + 0.5 is after now; adding 1 to the end would wrongly count it
    assert is_rate_limited([95, 100.5], 100, 10, 2, include_now=True) is False


def test_include_now_explicit_false():
    assert is_rate_limited([95, 100], 100, 10, 2, include_now=False) is False
