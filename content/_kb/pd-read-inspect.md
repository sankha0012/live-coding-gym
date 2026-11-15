---
title: Reading and inspecting a DataFrame
summary: Load a CSV with read_csv and take a first look with shape, head, dtypes, info, isna and value_counts.
tags: [pandas, csv, inspection]
---
```python
import pandas as pd
orders = pd.read_csv("content/_shared/orders.csv")
orders.shape                        # (1500, 11)   rows, columns
orders.head(3)                      # first 3 rows as a DataFrame
orders.dtypes                       # one dtype per column
orders.isna().sum()                 # missing per column: subtotal 7, coupon_code 1010
orders["status"].value_counts()     # delivered 1392, cancelled 108
orders["subtotal"].describe()       # count 1493, mean 79.40, min 21.10, max 182.42
orders["restaurant_id"].nunique()   # 24
```

- `shape` and `dtypes` are attributes (no brackets); `head()`, `info()` and `describe()` are methods.
- `read_csv` guesses the dtypes. Dates come in as text unless you ask for `parse_dates`.
- Check `shape`, `dtypes` and `isna().sum()` before you compute anything.

<!-- more -->

## Details

`read_csv` takes options that save work later:

```python
small = pd.read_csv(
    "content/_shared/orders.csv",
    usecols=["order_id", "created_at", "subtotal"],  # only these columns
    parse_dates=["created_at"],                      # datetime64 instead of text
    nrows=5,                                         # only the first 5 rows
)
small.shape                # (5, 3)
small["created_at"].dtype  # datetime64[us]
```

A whole-number column with missing values is read as `float64`, because NaN is a float. `courier_id` is an example. Pass `dtype={"courier_id": "Int64"}` (capital I) to keep integers with missing values.

`orders.info()` prints the dtypes and the non-null count of every column in one table. It prints and returns `None`.

`describe()` covers numeric columns only. Its `count` skips missing values, so 1493 here and not 1500.

`value_counts()` sorts by count, largest first, and drops missing values:

```python
orders["status"].value_counts(normalize=True)       # delivered 0.928, cancelled 0.072
orders["coupon_code"].value_counts(dropna=False)    # NaN 1010, FRETEGRATIS 243, ...
orders.select_dtypes("number").columns.tolist()     # the 8 numeric column names
orders.sample(3, random_state=0)                    # 3 random rows, repeatable
```

`orders.columns.tolist()` gives the column names as a plain list. `orders.tail(3)` shows the last rows.

## Common mistakes

- Writing `orders.shape()` or `orders.dtypes()`. They are attributes, not methods.
- Trusting `head()` alone. Missing values and bad rows often sit further down, so run `isna().sum()` too.
- Forgetting that `value_counts()` hides missing values unless you pass `dropna=False`.
- Treating `created_at` as a date straight after `read_csv`. It is text until you parse it.

## See also

- [dtypes, astype and datetimes](#/kb/pd-dtypes-datetime)
- [Missing values: isna, fillna, dropna](#/kb/pd-missing-values)
- [Selecting and filtering rows and columns](#/kb/pd-select-filter)
- Official docs: https://pandas.pydata.org/docs/
