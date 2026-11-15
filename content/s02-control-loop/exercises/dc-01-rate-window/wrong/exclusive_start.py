from eventwin import window_slice


def is_rate_limited(timestamps, now, window, limit):
    # assumes the lower bound is exclusive and shifts it
    recent = window_slice(timestamps, now - window + 1, now)
    return len(recent) >= limit
