---
title: dtypes, astype and datetimes
summary: Check and convert column types with astype, to_numeric and to_datetime, then use the .dt accessor on dates.
tags: [pandas, dtypes, datetime]
---
```python
import pandas as pd
orders = pd.read_csv("content/_shared/orders.csv")
orders["created_at"].dtype                 # str   text, not a date yet
orders["created_at"] = pd.to_datetime(orders["created_at"])
c = orders["created_at"]                   # dtype datetime64[us]
c.dt.year.iloc[0], c.dt.hour.iloc[0]       # (2026, 23)   first row is 2026-10-12 23:37
c.dt.day_name().iloc[0]                    # 'Monday'
c.dt.strftime("%Y-%m").iloc[0]             # '2026-10'
len(orders[c >= "2026-10-01"])             # 524   compare with a date string
orders["courier_id"].astype("Int64")       # 58, 6, ...  integers that allow missing
```

- `.dt` only works on a datetime column. Convert with `pd.to_datetime` first.
- `astype` fails on bad values. `pd.to_numeric(..., errors="coerce")` turns them into NaN.
- `astype` returns a new Series. Assign it back.

<!-- more -->

## Details

`orders.dtypes` lists the type of each column: `int64`, `float64`, `bool`, `datetime64`, and `str` for text (older pandas shows text as `object`).

Common conversions:

```python
orders["order_id"].astype(str).iloc[0]            # '100001'
(orders["subtotal"] > 100).astype(int).sum()      # 360   True/False to 1/0
orders["status"].astype("category").cat.categories.tolist()   # ['cancelled', 'delivered']
pd.to_numeric(pd.Series(["1", "2", "x"]), errors="coerce").tolist()   # [1.0, 2.0, nan]
pd.to_datetime(pd.Series(["2026-01-05", "bad"]), errors="coerce")     # 2026-01-05, NaT
```

`NaT` is the missing value for dates. `isna()` finds it.

More `.dt` parts: `month`, `day`, `day_of_week` (Monday is 0), `date`, `floor("D")` (midnight of that day), `to_period("M")`.

Subtracting two datetimes gives a `Timedelta`:

```python
span = c.max() - c.min()            # Timedelta('91 days 22:47:00')
span.days                           # 91
span.total_seconds() / 3600         # 2206.78... hours
(c - pd.Timestamp("2026-08-01")).dt.days.iloc[0]         # 72
pd.Timestamp("2026-10-12 23:37") + pd.Timedelta(minutes=30)   # 2026-10-13 00:07:00
```

Ambiguous formats need `format`. `pd.to_datetime("05/01/2026")` is read month first, 1 May. With `format="%d/%m/%Y"` it is 5 January.

Time zones: `c.dt.tz_localize("UTC").dt.tz_convert("America/Sao_Paulo")` turns 23:37 UTC into 20:37-03:00. Localize says what zone naive times are in. Convert moves them to another zone.

## Common mistakes

- Using `.dt` on a text column: `AttributeError: Can only use .dt accessor with datetimelike values`.
- Calling `astype(int)` on a column with missing values. It raises. Use `"Int64"` or fill first.
- Comparing date strings as text. It only works by accident for ISO format. Parse first.
- Filtering a month with `<= "2026-09-30"`. That stops at midnight and loses the last day. Use `< "2026-10-01"`.
- Forgetting `parse_dates=["created_at"]` in `read_csv` and then sorting text.

## See also

- [Reading and inspecting a DataFrame](#/kb/pd-read-inspect)
- [rolling and resample](#/kb/pd-rolling)
- [Missing values: isna, fillna, dropna](#/kb/pd-missing-values)
- [Dates and times: datetime, timedelta, zoneinfo](#/kb/py-datetime)
- Official docs: https://pandas.pydata.org/docs/
