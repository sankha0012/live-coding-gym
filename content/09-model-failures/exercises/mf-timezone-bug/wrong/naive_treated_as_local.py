from datetime import datetime
from zoneinfo import ZoneInfo


def daily_counts(timestamps, tz_name):
    tz = ZoneInfo(tz_name)
    counts = {}
    for ts in timestamps:
        local = ts.astimezone(tz) if ts.tzinfo else ts.replace(tzinfo=tz)
        key = local.date().isoformat()
        counts[key] = counts.get(key, 0) + 1
    return counts
