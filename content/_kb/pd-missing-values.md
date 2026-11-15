---
title: "Missing values: isna, fillna, dropna"
summary: Find missing values with isna, replace them with fillna, or remove the rows with dropna.
tags: [pandas, missing values, nan]
---
```python
import numpy as np
import pandas as pd
s = pd.Series([1.0, np.nan, 3.0])
s.isna()               # [False, True, False]
s.isna().sum()         # 1      count of missing
s.fillna(0)            # [1.0, 0.0, 3.0]
s.fillna(s.median())   # [1.0, 2.0, 3.0]
s.dropna()             # [1.0, 3.0]  index labels 0 and 2
s.mean()               # 2.0    NaN is skipped, not counted as 0
s.count(), len(s)      # (2, 3)
```

- Test for missing with `isna()` / `notna()`. Never with `== np.nan`, which is always `False`.
- `fillna` and `dropna` return a new object. Assign the result back.
- `sum`, `mean`, `count` skip NaN by default.

<!-- more -->

## Details

On a DataFrame, `isna().sum()` counts per column and `isna().mean()` gives the missing share:

```python
orders = pd.read_csv("content/_shared/orders.csv")
orders.isna().sum()     # courier_id 108, subtotal 7, coupon_code 1010, actual_minutes 108
orders["coupon_code"].isna().mean()            # 0.673...
len(orders.dropna())                           # 451   any missing value drops the row
len(orders.dropna(subset=["subtotal"]))        # 1493  only look at subtotal
```

Fill different columns with different values by passing a dict, or fill one column at a time:

```python
clean = orders.fillna({"coupon_code": "NONE", "subtotal": 0})
orders["subtotal"] = orders["subtotal"].fillna(orders["subtotal"].median())   # median is 76.77
orders["has_coupon"] = orders["coupon_code"].notna()                          # 490 True
```

Think about what a missing value means before filling. `actual_minutes` is missing for cancelled orders, because nothing was delivered. Filling it with 0 changes the mean from 41.88 to 38.86, which is wrong. A flag column such as `has_coupon` often keeps more information than a fill.

`s.ffill()` carries the last seen value forward: `[1.0, 1.0, 3.0]`. It only makes sense on sorted time data.

`None` in a numeric column becomes NaN and the column becomes `float64`. Use `dtype="Int64"` for integers with missing values, shown as `<NA>`. `pd.isna(x)` works on a single value, including `None`.

A sum over only missing values is `0.0`. Pass `skipna=False` to get NaN when anything is missing.

## Common mistakes

- Calling `df.dropna()` with no `subset`. Here it throws away 1049 of 1500 rows because most orders have no coupon.
- Writing `df["x"].fillna(0)` without assigning it back, so nothing changes.
- Filling with the mean or median of the whole dataset before a train/test split. Compute it on the training rows only.
- Comparing with `== np.nan` or `== None`.
- Forgetting that comparisons with NaN are `False`, so those rows drop out of every filter.

## See also

- [Reading and inspecting a DataFrame](#/kb/pd-read-inspect)
- [dtypes, astype and datetimes](#/kb/pd-dtypes-datetime)
- [Floats, NaN, infinity and rounding](#/kb/py-math-nan)
- Official docs: https://pandas.pydata.org/docs/
