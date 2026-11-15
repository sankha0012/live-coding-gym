from eventwin import window_slice


def is_rate_limited(timestamps, now, window, limit, *, include_now=False):
    recent = window_slice(timestamps, now - window, now, inclusive_end=include_now)
    return len(recent) >= limit
