---
title: "Dates and times: datetime, timedelta, zoneinfo"
summary: Parse, format, add and compare dates and times, and handle time zones with ZoneInfo.
tags: [python, dates, time zones]
---
```python
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
d = datetime.fromisoformat("2024-03-15T10:30:00")   # datetime(2024, 3, 15, 10, 30)  naive
d.strftime("%Y-%m-%d %H:%M")                    # '2024-03-15 10:30'   datetime -> str
datetime.strptime("15/03/2024", "%d/%m/%Y")     # datetime(2024, 3, 15, 0, 0)   str -> datetime
d + timedelta(days=20, hours=2)                 # datetime(2024, 4, 4, 12, 30)
a = d.replace(tzinfo=ZoneInfo("Europe/Madrid")) # aware: has a time zone
a.astimezone(timezone.utc).isoformat()          # '2024-03-15T09:30:00+00:00'
```

- `strftime` formats (f for format), `strptime` parses (p for parse).
- Subtracting two datetimes gives a `timedelta`. Adding a `timedelta` gives a datetime.
- A naive datetime has no time zone. An aware one does. You cannot compare or subtract one from the other.

<!-- more -->

## Details

`fromisoformat` reads ISO 8601 text and `isoformat()` writes it. If the text has an offset or `Z`, the result is aware:

```python
datetime.fromisoformat("2024-03-15T10:30:00Z")
# datetime(2024, 3, 15, 10, 30, tzinfo=timezone.utc)
datetime.fromisoformat("2024-03-15T10:30:00").tzinfo   # None  (naive)
```

Common format codes: `%Y` year, `%m` month, `%d` day, `%H` hour (24h), `%M` minute, `%S` second, `%A` weekday name, `%B` month name.

`timedelta` stores days, seconds and microseconds. Use `total_seconds()` for the full length:

```python
(datetime(2024, 3, 15) - datetime(2024, 3, 1)).days   # 14
td = timedelta(hours=36)
td.days, td.seconds, td.total_seconds()               # (1, 43200, 129600.0)
```

`d.date()` drops the time. `d.weekday()` is 0 for Monday and 6 for Sunday.

Time zones:

- `datetime.now(timezone.utc)` is the current time as an aware UTC value. Plain `datetime.now()` is naive local time.
- `replace(tzinfo=...)` attaches a zone without changing the clock numbers.
- `astimezone(...)` converts to another zone: same instant, different clock numbers.
- `ZoneInfo("Europe/Madrid")` knows about daylight saving time. A fixed offset does not.

A good rule: store and compare in UTC, convert to a local zone only to display.

## Common mistakes

- Mixing naive and aware values: `TypeError: can't compare offset-naive and offset-aware datetimes`.
- Using `.seconds` when you mean `.total_seconds()`. `.seconds` ignores whole days.
- Swapping `%m` (month) and `%M` (minute), or `%d` and `%D`.
- Using `replace(tzinfo=...)` when you wanted to convert. It relabels, it does not shift the time.
- Calling `datetime.now()` inside logic you need to test. Pass the current time in as a parameter.

## See also

- [Clocks: time.monotonic and injecting a clock or sleep](#/kb/py-time-clock-injection)
- [f-strings and number formatting](#/kb/py-f-strings)
- [Dates in SQLite: strftime, date, julianday](#/kb/sql-dates-sqlite)
- Official docs: https://docs.python.org/3/library/datetime.html
