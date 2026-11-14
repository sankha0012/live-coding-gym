from datetime import datetime, timedelta, timezone


def daily_counts(timestamps, tz_name):
    offsets = {"America/Sao_Paulo": -3, "America/New_York": -5}
    tz = timezone(timedelta(hours=offsets[tz_name]))
    counts = {}
    for ts in timestamps:
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        key = ts.astimezone(tz).date().isoformat()
        counts[key] = counts.get(key, 0) + 1
    return counts
