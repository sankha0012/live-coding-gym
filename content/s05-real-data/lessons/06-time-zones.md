# Time zones and naive datetimes

## What it is

A naive datetime has no zone: `2026-03-08 23:30` could be anywhere. An aware datetime carries its zone or offset. Production systems should store and compare instants in UTC and convert to a local zone only to show them or to define a local day. See [dtypes and datetimes](#/kb/pd-dtypes-datetime) and [Python datetime](#/kb/py-datetime).

## How it breaks in production

- **Mixing.** Subtracting a naive and an aware timestamp raises `TypeError`, in pandas and in plain `datetime`.
- **Wrong day.** An order at 02:30 UTC on 8 March happened at 23:30 on 7 March in Sao Paulo. Daily totals by UTC date and by local date disagree.
- **The server's clock.** `datetime.now()` is naive and uses the machine's zone, so the same code gives different results on a laptop and on a server.
- **Daylight saving time.** In a zone with DST, one local hour does not exist in spring and one happens twice in autumn.

## The defence in code

```python
import pandas as pd

utc = pd.Series(pd.to_datetime(["2026-03-08 02:30", "2026-03-09 01:30"])).dt.tz_localize("UTC")
sp = utc.dt.tz_convert("America/Sao_Paulo")
print(utc.dt.date.tolist())   # 8 March, 9 March
print(sp.dt.date.tolist())    # 7 March, 8 March

try:
    utc.iloc[0] - pd.Timestamp("2026-03-08")
except TypeError as e:
    print("TypeError:", e)

def to_utc(s, tz):
    return pd.to_datetime(s).dt.tz_localize(tz).dt.tz_convert("UTC")

print(to_utc(pd.Series(["2026-03-08 23:30"]), "America/Sao_Paulo").tolist())

try:
    pd.Timestamp("2026-11-01 01:30").tz_localize("America/New_York")
except ValueError as e:
    print("ambiguous:", e)
```

The same two instants fall on different calendar days depending on the zone, which is why I decide which day definition the business uses before grouping. Mixing naive and aware raises an error, which is the good outcome. `to_utc` declares what zone the naive text was written in and converts, so 23:30 in Sao Paulo becomes 02:30 the next day in UTC. The last block shows pandas refusing an ambiguous autumn time in New York instead of guessing.

## What to say in the interview

"I keep all stored timestamps in UTC and aware, and I convert to local time only to define a business day or to display. When I read naive text I ask which zone it was written in and localize it explicitly. I avoid `datetime.now()` without a zone, and I inject the clock so that tests are deterministic."
