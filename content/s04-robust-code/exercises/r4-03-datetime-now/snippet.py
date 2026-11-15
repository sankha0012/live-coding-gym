from datetime import datetime, timedelta

events = [
    datetime(2024, 2, 20, 8, 0),
    datetime(2024, 3, 1, 10, 0),
    datetime(2024, 3, 3, 9, 30),
    datetime(2024, 3, 4, 23, 0),
]


def last_week_events(events, days=7):
    end = datetime.now()
    start = end - timedelta(days=days)
    return [e for e in events if start <= e <= end]


def last_week_events_at(events, now, days=7):
    start = now - timedelta(days=days)
    return [e for e in events if start <= e <= now]


fixed_now = datetime(2024, 3, 5, 12, 0)

print("with datetime.now():", len(last_week_events(events)))
print("with now=2024-03-05 12:00:", len(last_week_events_at(events, fixed_now)))
print("same again:", len(last_week_events_at(events, fixed_now)))
