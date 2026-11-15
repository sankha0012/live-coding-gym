from datetime import timezone


def is_expired(expires_at, now):
    """True if now is at or after expires_at.

    Naive datetimes are treated as UTC. Aware datetimes are converted to UTC.
    """
    expires_at = expires_at.replace(tzinfo=timezone.utc)
    now = now.replace(tzinfo=timezone.utc)
    return now >= expires_at
