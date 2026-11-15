"""Small helper for working with event timestamps (seconds)."""


def window_slice(timestamps, start, end, *, inclusive_end=False):
    """Return the timestamps t with start <= t < end (start <= t <= end when
    inclusive_end is true), in their original order."""
    if end < start:
        raise ValueError("end must not be before start")
    if inclusive_end:
        return [t for t in timestamps if start <= t <= end]
    return [t for t in timestamps if start <= t < end]
