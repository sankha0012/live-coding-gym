def is_expired(expires_at, now):
    return now.replace(tzinfo=None) >= expires_at.replace(tzinfo=None)
