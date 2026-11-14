from datetime import timezone


def _utc(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def is_expired(expires_at, now):
    """True if now is at or after expires_at.

    Naive datetimes are treated as UTC. Aware datetimes are converted to UTC.
    """
    return _utc(now) >= _utc(expires_at)
