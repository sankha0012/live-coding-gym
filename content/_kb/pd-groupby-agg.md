---
title: groupby and aggregation
summary: Split rows into groups by key, then reduce each group with mean, sum, count, size or named aggregations.
tags: [pandas, groupby, aggregation]
---
```python
import pandas as pd
orders = pd.read_csv("content/_shared/orders.csv")
orders.groupby("status")["subtotal"].mean()   # cancelled 86.07, delivered 78.88
orders.groupby("status").size()               # cancelled 108, delivered 1392  (rows)
per_rest = orders.groupby("restaurant_id").agg(
    n_orders=("order_id", "count"),
    revenue=("subtotal", "sum"),
    avg_minutes=("actual_minutes", "mean"),
)                                             # 24 rows, index = restaurant_id
per_rest.loc[1]                               # n_orders 34, revenue 2592.78, avg_minutes 42.50
```

- Pattern: `df.groupby(keys)[column].function()`.
- The group keys become the index. Add `as_index=False` or `.reset_index()` to get them back as columns.
- `size()` counts rows. `count()` counts non-missing values.

<!-- more -->

## Details

Named aggregation is `new_name=(column, function)`. The function is a string such as `"sum"`, `"mean"`, `"count"`, `"min"`, `"max"`, `"median"`, `"nunique"`, or any callable.

Several functions on one column:

```python
orders.groupby("status")["subtotal"].agg(["count", "mean", "max"])
#            count   mean     max
# cancelled    107  86.07  169.60
# delivered   1386  78.88  182.42
```

`count` is 107 and not 108 because one cancelled order has a missing `subtotal`.

Group by several keys with a list. The result has a MultiIndex, so `reset_index` is usually the next step:

```python
orders.groupby(["status", "promised_minutes"]).size().reset_index(name="n")
#       status  promised_minutes   n
# 0  cancelled                30  29
# 1  cancelled                40  39  ...
```

`transform` returns one value per original row, so you can add a group statistic as a column:

```python
orders["rest_avg"] = orders.groupby("restaurant_id")["subtotal"].transform("mean")
len(orders)   # 1500, same rows as before
```

Top groups: sort the result.

```python
orders.groupby("restaurant_id")["subtotal"].sum().sort_values(ascending=False).head(3)
# restaurant 5: 10501.17, 7: 10097.23, 4: 10089.30
```

Rows whose key is missing are dropped. `groupby("coupon_code").size()` adds up to 490. Pass `dropna=False` to keep a NaN group of 1010.

## Common mistakes

- Forgetting the column: `orders.groupby("status").mean()` tries every column and fails on text columns.
- Using `count()` when you want the number of rows. Use `size()`.
- Expecting the key to be a column afterwards. It is the index until you call `reset_index()`.
- Reading a mean over missing values as zero. A group with only missing values gives NaN: mean `actual_minutes` for cancelled orders is NaN.
- Losing the rows with a missing key without noticing.

## See also

- [pivot_table and crosstab](#/kb/pd-pivot)
- [merge: joins, row counts and validate](#/kb/pd-merge)
- [sort_values and drop_duplicates](#/kb/pd-sort-dedupe)
- [GROUP BY and aggregate functions](#/kb/sql-group-by)
- Official docs: https://pandas.pydata.org/docs/
