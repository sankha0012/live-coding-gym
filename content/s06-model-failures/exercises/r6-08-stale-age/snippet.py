from datetime import datetime, timedelta

NOW = datetime(2026, 11, 15, 12, 0)
MAX_AGE = timedelta(days=7)

def stale_by_days(trained_at):
    return (NOW - trained_at).days > 7

def stale_by_delta(trained_at):
    return NOW - trained_at > MAX_AGE

for name, trained in [
    ("m1", datetime(2026, 11, 10, 12, 0)),
    ("m2", datetime(2026, 11, 7, 13, 0)),
    ("m3", datetime(2026, 11, 8, 12, 0)),
    ("m4", datetime(2026, 11, 20, 12, 0)),
]:
    age = NOW - trained
    print(name, age, stale_by_days(trained), stale_by_delta(trained))
