from eventwin import window_slice


def is_rate_limited(timestamps, now, window, limit):
    # assumes the upper bound is inclusive and widens it
    recent = window_slice(timestamps, now - window, now + 1)
    return len(recent) >= limit
