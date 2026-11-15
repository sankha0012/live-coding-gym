---
title: Selecting and filtering rows and columns
summary: Pick columns with [] and rows with a boolean mask, .loc (labels) or .iloc (positions).
tags: [pandas, filtering, loc]
---
```python
import pandas as pd
orders = pd.read_csv("content/_shared/orders.csv")
orders["subtotal"]                    # one column -> Series
orders[["order_id", "subtotal"]]      # list of columns -> DataFrame, shape (1500, 2)
big = orders[orders["subtotal"] > 100]                    # 360 rows
mask = (orders["status"] == "delivered") & (orders["subtotal"] > 100)
orders[mask]                          # 321 rows
orders.loc[mask, ["order_id", "subtotal"]]   # rows by mask, columns by name
orders.iloc[:2, :3]                   # first 2 rows, first 3 columns, by position
```

- Combine conditions with `&`, `|`, `~` and put each condition in brackets.
- `.loc` uses labels and includes the end of a slice. `.iloc` uses positions and excludes it.
- A filter keeps the original index labels. Use `reset_index(drop=True)` for 0, 1, 2...

<!-- more -->

## Details

A comparison on a column gives a boolean Series, the mask. Indexing with the mask keeps the rows where it is `True`.

Useful mask builders:

```python
orders[orders["coupon_code"].isin(["PIZZA20", "BEMVINDO10"])]        # 247 rows
orders[~orders["coupon_code"].isin(["PIZZA20", "BEMVINDO10"])]       # 1253 rows
orders[orders["subtotal"].between(50, 100)]                          # 846 rows, both ends included
orders[orders["coupon_code"].str.startswith("PIZZA", na=False)]      # 89 rows
orders.query("status == 'delivered' and subtotal > 100")             # 321 rows
```

`.loc[rows, columns]` is also how you read or write single cells and conditional updates:

```python
orders.loc[0, "subtotal"]          # 79.29   row label 0
orders.iloc[0, 5]                  # 79.29   row position 0, column position 5
orders.loc[0:2].shape              # (3, 11) label slice includes 2
orders.iloc[0:2].shape             # (2, 11) position slice excludes 2
df = orders.copy()
df.loc[df["delivery_fee"] == 0, "free_delivery"] = True   # sets 345 rows
```

After filtering, `big.index` starts `[4, 5, 7]`. So `big.loc[0]` raises `KeyError`, while `big.iloc[0]` is the first row.

A missing value compares as `False`, so rows with a missing `subtotal` are dropped by `subtotal > 100` and also by `subtotal <= 100`.

## Common mistakes

- Using `and` / `or` between masks. It raises `ValueError: The truth value of a Series is ambiguous`. Use `&` / `|`.
- Leaving out the brackets: `a == 1 & b > 2` is parsed as `a == (1 & b) > 2`.
- Chained assignment such as `df[mask]["col"] = 1`. It writes to a temporary copy and the original is unchanged. Use `df.loc[mask, "col"] = 1`.
- Writing `orders["a", "b"]` for two columns. It needs a list: `orders[["a", "b"]]`.
- Using `.loc[0]` after a filter and expecting the first row.

## See also

- [Reading and inspecting a DataFrame](#/kb/pd-read-inspect)
- [Missing values: isna, fillna, dropna](#/kb/pd-missing-values)
- [sort_values and drop_duplicates](#/kb/pd-sort-dedupe)
- Official docs: https://pandas.pydata.org/docs/
