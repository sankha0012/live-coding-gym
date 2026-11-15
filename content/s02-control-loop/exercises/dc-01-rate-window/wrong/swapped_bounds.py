from eventwin import window_slice


def is_rate_limited(timestamps, now, window, limit):
    recent = window_slice(timestamps, now, now - window)
    return len(recent) >= limit
