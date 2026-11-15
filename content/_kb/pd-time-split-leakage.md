---
title: Time-based splits and leakage
summary: Split data by time so training rows come before test rows, and build features only from the past.
tags: [pandas, time split, leakage]
---
```python
import pandas as pd
orders = pd.read_csv("content/_shared/orders.csv", parse_dates=["created_at"])
o = orders.sort_values("created_at").reset_index(drop=True)
cutoff = pd.Timestamp("2026-10-01")
train = o[o["created_at"] < cutoff]       # 976 rows, last one 2026-09-30 22:38
test = o[o["created_at"] >= cutoff]       # 524 rows, first one 2026-10-01 02:59
n = int(len(o) * 0.8)                     # or split by position after sorting
train80, test20 = o.iloc[:n], o.iloc[n:]  # 1200 and 300 rows
```

- Sort by time, then cut. Everything in train must happen before everything in test.
- Use `<` on one side and `>=` on the other so no row is in both or in neither.
- A feature may only use information that existed at the time of the row.

<!-- more -->

## Details

A random split mixes future rows into training. The model then looks better in the test than it will in production, where it only ever sees the past. This is leakage.

Check the split after making it:

```python
train["created_at"].max() < test["created_at"].min()    # True
len(train) + len(test) == len(o)                        # True
```

Leakage also hides in features. A group average over all rows uses the future of each row:

```python
o["leaky"] = o.groupby("customer_id")["subtotal"].transform("mean")
# customer 33: 67.66 on every row, including the first order
```

The safe version only uses earlier rows. `shift(1)` removes the current row, `expanding()` takes everything before it:

```python
o["avg_before"] = o.groupby("customer_id")["subtotal"].transform(
    lambda x: x.shift(1).expanding().mean()
)
# customer 33: subtotals 64.28, 85.92, 103.81 -> avg_before NaN, 64.28, 75.10
o["orders_before"] = o.groupby("customer_id").cumcount()   # 0, 1, 2, ...
```

The first row of each customer is NaN, because there is no history yet. That is correct. Do not fill it with a value computed from later rows.

Statistics used for cleaning follow the same rule. Compute medians, means and outlier limits on `train`, then apply them to `test`.

Columns that are only known after the outcome are leaks too. `actual_minutes` cannot be a feature for predicting lateness at order time.

For cross-validation on time data, `sklearn.model_selection.TimeSeriesSplit` gives growing training windows. With 10 rows and 3 splits the test folds are rows `[4 5]`, `[6 7]` and `[8 9]`, each trained on all rows before them.

## Common mistakes

- Using `train_test_split` with its default shuffle on time-ordered data.
- Splitting by position without sorting by time first.
- Building features on the full frame before the split, with `transform("mean")` or a `merge` of totals.
- Using `<=` on both sides of the cutoff, which puts boundary rows in both sets.
- Leaving the same customer's later rows to inform their earlier rows through target encoding.

## See also

- [rolling and resample](#/kb/pd-rolling)
- [Train/test splits and data leakage](#/kb/ml-train-test-split-leakage)
- [Cross-validation](#/kb/ml-cross-validation)
- [dtypes, astype and datetimes](#/kb/pd-dtypes-datetime)
