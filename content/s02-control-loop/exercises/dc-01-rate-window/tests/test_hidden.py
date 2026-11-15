from solution import is_rate_limited


def test_under_limit():
    assert is_rate_limited([95, 98], 100, 10, 3) is False


def test_at_limit():
    assert is_rate_limited([95, 98, 99], 100, 10, 3) is True


def test_request_exactly_at_window_start_counts():
    # window is [90, 100): 90 is inside
    assert is_rate_limited([90, 95], 100, 10, 2) is True


def test_request_just_before_window_start_does_not_count():
    assert is_rate_limited([89, 95], 100, 10, 2) is False


def test_request_exactly_at_now_does_not_count():
    assert is_rate_limited([100, 95], 100, 10, 2) is False


def test_unsorted_input():
    assert is_rate_limited([99, 91, 50, 97], 100, 10, 3) is True


def test_empty_history():
    assert is_rate_limited([], 100, 10, 1) is False


def test_zero_window_is_never_limited():
    assert is_rate_limited([100, 99], 100, 0, 1) is False
