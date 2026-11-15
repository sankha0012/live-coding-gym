---
title: pivot_table and crosstab
summary: Turn one key into rows and another into columns, aggregating a value (pivot_table) or counting (crosstab).
tags: [pandas, pivot, reshape]
---
```python
import pandas as pd
orders = pd.read_csv("content/_shared/orders.csv")
rest = pd.read_csv("content/_shared/restaurants.csv")
df = orders.merge(rest, on="restaurant_id", how="left")
pt = df.pivot_table(index="city", columns="status", values="subtotal", aggfunc="mean")
pt.loc["Sao Paulo"].round(2)             # cancelled 90.81, delivered 76.82
ct = pd.crosstab(df["city"], df["status"])
ct.loc["Sao Paulo"]                      # cancelled 25, delivered 382
```

- `index` becomes the rows, `columns` the column headers, `values` the cells, `aggfunc` how to combine them.
- `aggfunc` defaults to `"mean"`. Say what you want.
- `crosstab` takes Series, not column names, and counts rows by default.

<!-- more -->

## Details

`pivot_table` is a `groupby` on two keys followed by `unstack`. These give the same table:

```python
same = df.groupby(["city", "status"])["subtotal"].mean().unstack()
same.equals(pt)        # True
```

Useful options: `fill_value=0` for empty cells and `margins=True` for totals named `All`.

```python
df.pivot_table(index="city", columns="status", values="order_id",
               aggfunc="count", fill_value=0, margins=True)
# status          cancelled  delivered   All
# Belo Horizonte         27        349   376
# Curitiba               12        110   122
# Rio de Janeiro         44        551   595
# Sao Paulo              25        382   407
# All                   108       1392  1500
```

`crosstab` can give shares instead of counts. `normalize="index"` makes each row add up to 1:

```python
pd.crosstab(df["city"], df["status"], normalize="index").round(3)
# Curitiba   cancelled 0.098, delivered 0.902
```

Use `normalize="columns"` for column shares and `normalize="all"` for shares of the grand total.

The result has `city` as the index and `status` as the name of the column axis. `pt.reset_index()` gives a flat frame with columns `['city', 'cancelled', 'delivered']`.

To go back from wide to long, use `melt`:

```python
long = pt.reset_index().melt(id_vars="city", var_name="status", value_name="avg")
long.shape             # (8, 3)   4 cities x 2 statuses
```

`df.pivot(index=, columns=, values=)` only reshapes. It does not aggregate, so it raises `ValueError: Index contains duplicate entries` when a row and column pair appears twice. Use `pivot_table` when in doubt.

## Common mistakes

- Forgetting `aggfunc` and reading means as if they were sums or counts.
- Passing column names to `crosstab`: `pd.crosstab("city", "status")` does not work. Pass `df["city"]`.
- Missing keys are dropped. `pd.crosstab(df["city"], df["coupon_code"])` only covers the 490 orders with a coupon. Fill first with `fillna("NONE")` to count all 1500.
- Empty cells are NaN, not 0, unless you pass `fill_value=0`.
- Treating `city` as a column afterwards. It is the index until `reset_index()`.

## See also

- [groupby and aggregation](#/kb/pd-groupby-agg)
- [merge: joins, row counts and validate](#/kb/pd-merge)
- [Conditional aggregation (CASE inside SUM, AVG, COUNT)](#/kb/sql-conditional-aggregation)
- Official docs: https://pandas.pydata.org/docs/
