from datetime import datetime, timezone

deadline = datetime(2026, 3, 1, 12, 0)                       # naive, from a CSV
event = datetime(2026, 3, 1, 11, 30, tzinfo=timezone.utc)    # aware, from an API

try:
    print(event < deadline)
except TypeError as err:
    print("TypeError:", err)

fixed = deadline.replace(tzinfo=timezone.utc)
print(event < fixed)
print(event == deadline)
print(event.isoformat())
print(deadline.isoformat())
