from datetime import datetime
from zoneinfo import ZoneInfo


def daily_counts(timestamps: list[datetime], tz_name: str) -> dict[str, int]:
    """Count events per local calendar day in the timezone `tz_name`.

    Aware timestamps are converted to `tz_name` first. Naive timestamps are
    UTC. Keys are ISO dates like "2024-03-09". Empty input gives {}.
    """
    tz = ZoneInfo(tz_name)
    counts: dict[str, int] = {}
    for ts in timestamps:
        local = ts.replace(tzinfo=tz)
        key = local.date().isoformat()
        counts[key] = counts.get(key, 0) + 1
    return counts
