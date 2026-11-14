from datetime import timezone


def is_expired(expires_at, now):
    return now.astimezone(timezone.utc) >= expires_at.astimezone(timezone.utc)
