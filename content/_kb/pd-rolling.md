---
title: rolling and resample
summary: Compute moving-window statistics with rolling and regroup a time series into days, weeks or months with resample.
tags: [pandas, time series, rolling]
---
```python
import pandas as pd
s = pd.Series([1, 2, 3, 4, 5])
s.rolling(3).mean().tolist()                 # [nan, nan, 2.0, 3.0, 4.0]
s.rolling(3, min_periods=1).mean().tolist()  # [1.0, 1.5, 2.0, 3.0, 4.0]
s.expanding().mean().tolist()                # [1.0, 1.5, 2.0, 2.5, 3.0]  all rows so far
s.shift(1).tolist()                          # [nan, 1.0, 2.0, 3.0, 4.0]  previous row
s.diff().tolist()                            # [nan, 1.0, 1.0, 1.0, 1.0]
s.cumsum().tolist()                          # [1, 3, 6, 10, 15]
```

- `rolling(n)` uses the current row and the `n - 1` rows before it. The first rows are NaN until the window is full.
- `resample` needs a datetime index, or `on="column"`.
- Windows follow row order. Sort by time first.

<!-- more -->

## Details

`resample` is a `groupby` on time buckets. Common rules are `"h"`, `"D"`, `"W"` (weeks ending Sunday), `"MS"` (month start) and `"ME"` (month end).

```python
orders = pd.read_csv("content/_shared/orders.csv", parse_dates=["created_at"])
daily = orders.set_index("created_at")["subtotal"].resample("D").sum()
len(daily)                         # 92 days
daily.iloc[0].round(2)             # 2050.44 on 2026-08-01
daily.rolling(7).mean().iloc[6].round(2)   # 1417.01  first full 7-day average

orders.resample("MS", on="created_at")["order_id"].count()
# 2026-08-01 514, 2026-09-01 462, 2026-10-01 524
```

Resampling creates every bucket in the range, including empty ones. For an empty bucket `sum()` gives 0 and `mean()` gives NaN:

```python
t = pd.Series([5, 7], index=pd.to_datetime(["2026-01-01", "2026-01-03"]))
t.resample("D").sum().tolist()     # [5, 0, 7]
t.resample("D").mean().tolist()    # [5.0, nan, 7.0]
```

A rolling window can also be a time span when the index is a sorted datetime: `daily.rolling("7D").mean()`. A time window is never NaN at the start, because it uses whatever rows fall inside the span.

For a feature that must only use the past, shift before rolling, and do it per group:

```python
o = orders.sort_values("created_at")
o["prev3"] = o.groupby("customer_id")["subtotal"].transform(
    lambda x: x.shift(1).rolling(3, min_periods=1).mean()
)
# customer 33: subtotals 64.28, 85.92, 103.81 -> prev3 NaN, 64.28, 75.10
```

`rolling(3, center=True)` centres the window. It looks at the next row, so never use it for model features.

## Common mistakes

- Rolling over unsorted rows. The window is by position, not by date.
- Forgetting that `rolling(n)` includes the current row. For "previous n rows" add `shift(1)`.
- Rolling over the whole frame when each customer or restaurant needs its own window. Use `groupby` first.
- Calling `resample` on a frame with a plain integer index: `TypeError: Only valid with DatetimeIndex`.
- Using `rolling(7)` on data with missing days and calling it a 7-day average. Resample to daily first.

## See also

- [dtypes, astype and datetimes](#/kb/pd-dtypes-datetime)
- [Time-based splits and leakage](#/kb/pd-time-split-leakage)
- [groupby and aggregation](#/kb/pd-groupby-agg)
- [Running totals, moving averages and window frames](#/kb/sql-running-totals-frames)
- Official docs: https://pandas.pydata.org/docs/
