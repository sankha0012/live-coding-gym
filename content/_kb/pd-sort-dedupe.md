---
title: sort_values and drop_duplicates
summary: Order rows with sort_values and remove repeated rows or keys with drop_duplicates.
tags: [pandas, sorting, duplicates]
---
```python
import pandas as pd
df = pd.DataFrame({"user": ["a", "a", "b", "b", "b"],
                   "day":  [1, 2, 1, 3, 3],
                   "amt":  [10, 20, 5, 7, 7]})
df.sort_values("amt", ascending=False)     # index order 1, 0, 3, 4, 2
df.sort_values(["user", "amt"], ascending=[True, False])   # user A-Z, then amt high to low
df.duplicated().tolist()                   # [False, False, False, False, True]
df.drop_duplicates()                       # 4 rows: the full-row repeat (index 4) is gone
df.drop_duplicates("user")                 # index 0 and 2: first row per user
df.drop_duplicates("user", keep="last")    # index 1 and 4: last row per user
```

- Both return a new DataFrame. The original keeps its order and rows.
- `drop_duplicates(keys)` keeps the first row it sees, so sort first to control which one stays.
- The old index labels travel with the rows. Add `.reset_index(drop=True)` for 0, 1, 2...

<!-- more -->

## Details

"Latest row per key" is sort, then drop duplicates keeping the last:

```python
orders = pd.read_csv("content/_shared/orders.csv", parse_dates=["created_at"])
latest = orders.sort_values("created_at").drop_duplicates("customer_id", keep="last")
len(latest)                        # 303
orders["customer_id"].nunique()    # 303  one row per customer
```

Top rows have a shortcut:

```python
orders.nlargest(3, "subtotal")["order_id"].tolist()   # [101026, 101065, 100678]
orders.sort_values("subtotal", ascending=False).head(3)   # same rows
```

Top row per group: sort, then `groupby(...).head(1)`:

```python
df.sort_values(["user", "amt"], ascending=[True, False]).groupby("user").head(1)
#   user  day  amt
# 1    a    2   20
# 3    b    3    7
```

Missing values go to the end, for ascending and for descending sorts. Pass `na_position="first"` to change that.

`sort_values` is not stable by default with one key. Pass `kind="stable"` when rows with equal keys must keep their order, or add a second key as a tie-breaker so the result is deterministic.

Checks before and after: `df["user"].is_unique` is `False`, `df.duplicated("user").sum()` counts the extra rows, and `df.duplicated("user", keep=False)` marks every row of a repeated key.

`sort_index()` sorts by the index labels instead of a column.

## Common mistakes

- Calling `df.sort_values("amt")` and not assigning the result.
- Dropping duplicates on a key without sorting, then keeping an arbitrary row.
- Using `drop_duplicates()` with no key and expecting one row per user. With no key the whole row must match.
- Using `.loc[0]` after sorting to get the top row. Label 0 is still the old first row. Use `.iloc[0]`.
- Leaving ties to chance, so two runs give a different "top 3".

## See also

- [Selecting and filtering rows and columns](#/kb/pd-select-filter)
- [groupby and aggregation](#/kb/pd-groupby-agg)
- [merge: joins, row counts and validate](#/kb/pd-merge)
- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- Official docs: https://pandas.pydata.org/docs/
