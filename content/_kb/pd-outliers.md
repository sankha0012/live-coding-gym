---
title: Outliers with the IQR rule
summary: Flag values below Q1 - 1.5*IQR or above Q3 + 1.5*IQR, then drop, clip or keep them with a flag.
tags: [pandas, outliers, quantiles]
---
```python
import pandas as pd
x = pd.Series([10, 12, 11, 13, 12, 95])
q1, q3 = x.quantile([0.25, 0.75])            # 11.25, 12.75
iqr = q3 - q1                                # 1.5
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr   # 9.0, 15.0
is_outlier = (x < low) | (x > high)
x[is_outlier].tolist()                       # [95]
x[~is_outlier].tolist()                      # [10, 12, 11, 13, 12]   dropped
x.clip(low, high).tolist()                   # [10, 12, 11, 13, 12, 15]   capped
```

- IQR is the interquartile range: Q3 minus Q1, the width of the middle half of the data.
- The limits are `Q1 - 1.5 * IQR` and `Q3 + 1.5 * IQR`.
- Quartiles barely move when one value is extreme. Mean and standard deviation do.

<!-- more -->

## Details

`quantile` with a list returns a Series, which unpacks into two numbers. `quantile(0.5)` is the median.

In the example the mean is 25.5 and the median is 12.0. The single value 95 drags the mean and inflates the standard deviation to 34.06. That is why the z-score rule (`abs(z) > 3`) misses it: its z-score is only 2.04.

On the orders data:

```python
orders = pd.read_csv("content/_shared/orders.csv")
s = orders["actual_minutes"]
q1, q3 = s.quantile([0.25, 0.75])            # 32.8, 49.65
iqr = q3 - q1                                # 16.85
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr   # 7.525, 74.925
mask = (s < low) | (s > high)
mask.sum()                                   # 15 outliers, from 75.4 to 89.6 minutes
len(orders[~mask])                           # 1485
```

Three ways to handle them:

- Drop: `orders[~mask]`.
- Clip (also called winsorize): `s.clip(low, high)` caps the values and keeps the rows.
- Flag: `orders["slow"] = mask` keeps everything and lets the analysis decide.

Missing values are never flagged, because comparisons with NaN are `False`. So `orders[~mask]` keeps the 108 rows with a missing `actual_minutes`. The other spelling, `orders[s.between(low, high)]`, drops them and returns 1377 rows. Decide which one you mean.

An outlier is not always an error. A 90-minute delivery may be real and may be exactly what the business cares about. Say what you did and why.

## Common mistakes

- Computing the limits on the full data and then splitting. Compute them on the training rows and reuse them on the test rows.
- Mixing up the two signs: `q1 - 1.5 * iqr` and `q3 + 1.5 * iqr`.
- Using one global limit when groups differ a lot. Compute the limits per group with `groupby(...).transform`.
- Dropping outliers silently and not reporting how many rows went.

## See also

- [Selecting and filtering rows and columns](#/kb/pd-select-filter)
- [Missing values: isna, fillna, dropna](#/kb/pd-missing-values)
- [Time-based splits and leakage](#/kb/pd-time-split-leakage)
- Official docs: https://pandas.pydata.org/docs/
