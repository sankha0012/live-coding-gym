"""Backoff delay helper for retry loops."""


def backoff_delay(attempt, base_ms, cap_ms, factor=2):
    """Seconds to wait after failed attempt number `attempt` (1-based)."""
    if attempt < 1:
        raise ValueError("attempt starts at 1")
    return min(base_ms * factor ** (attempt - 1), cap_ms) / 1000
