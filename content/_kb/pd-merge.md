---
title: "merge: joins, row counts and validate"
summary: Join two DataFrames on a key with merge, choose the join type with how, and guard the row count with validate.
tags: [pandas, merge, joins]
---
```python
import pandas as pd
orders = pd.read_csv("content/_shared/orders.csv")
rest = pd.read_csv("content/_shared/restaurants.csv")
df = orders.merge(rest, on="restaurant_id", how="left", validate="many_to_one")
df.shape                   # (1500, 14)  11 order columns + name, city, cuisine
len(df) == len(orders)     # True  a many-to-one left join never adds rows
df.groupby("city")["subtotal"].sum()   # Rio de Janeiro 46911.65, Sao Paulo 31387.00, ...
```

- `how` is `"inner"` (default), `"left"`, `"right"` or `"outer"`.
- A duplicated key on the right side multiplies the left rows. Compare `len` before and after.
- `validate="many_to_one"` raises `MergeError` if the right key is not unique.

<!-- more -->

## Details

Two tiny frames show every join type. Key 1 appears twice on the right, key 4 only on the right.

```python
left = pd.DataFrame({"k": [1, 2, 3], "a": ["x", "y", "z"]})
right = pd.DataFrame({"k": [1, 1, 4], "b": [10, 11, 40]})
len(left.merge(right, on="k"))                # 2  inner: k=1 twice
len(left.merge(right, on="k", how="left"))    # 4  all left rows, k=1 doubled
len(left.merge(right, on="k", how="right"))   # 3  all right rows
len(left.merge(right, on="k", how="outer"))   # 5  everything
```

Rows with no match get NaN in the other side's columns. That turns an integer column into float: `b` becomes `10.0, 11.0, NaN, NaN` in the left join.

`indicator=True` adds a `_merge` column with `both`, `left_only` or `right_only`. It gives the anti-join:

```python
m = left.merge(right, on="k", how="left", indicator=True)
m[m["_merge"] == "left_only"][["k", "a"]]     # rows k=2 and k=3: no match on the right
```

When the key names differ, use `left_on` and `right_on`. Both key columns are kept. When a non-key column exists on both sides, pandas adds `_x` and `_y`. Choose your own with `suffixes=("_left", "_right")`.

`validate` accepts `"one_to_one"`, `"one_to_many"`, `"many_to_one"` and `"many_to_many"`. The first word describes the left key.

`pd.concat([a, b], ignore_index=True)` stacks rows. It is not a join.

## Common mistakes

- Not checking the row count. One duplicated key on the lookup table silently inflates sums.
- Using the default inner join and losing the rows that have no match.
- Merging keys of different dtypes. Integer against text raises `ValueError`. Convert one side with `astype` first.
- Forgetting `on=`. pandas then joins on every column name the two frames share.
- Summing a column after a one-to-many merge, which counts the "one" side several times.

## See also

- [groupby and aggregation](#/kb/pd-groupby-agg)
- [sort_values and drop_duplicates](#/kb/pd-sort-dedupe)
- [Missing values: isna, fillna, dropna](#/kb/pd-missing-values)
- [INNER JOIN](#/kb/sql-joins)
- Official docs: https://pandas.pydata.org/docs/
