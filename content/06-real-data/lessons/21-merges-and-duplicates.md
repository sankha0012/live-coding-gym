# Merges and duplicates

## The problem it solves

A join should add columns. It must not change how many orders you have. When it does, every sum after it is wrong, and nothing crashes to warn you. Revenue is just quietly too high. This is the most common silent bug in analysis code, and interviewers know it.

The habit: write down the row count before the merge, state what you expect after, and check.

## The smallest runnable example

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3],
    "restaurant_id": [10, 10, 20],
    "gmv": [100.0, 50.0, 80.0],
})
restaurants = pd.DataFrame({
    "restaurant_id": [10, 20, 20],      # 20 appears twice by mistake
    "city": ["SP", "RJ", "RJ"],
})

merged = orders.merge(restaurants, on="restaurant_id", how="left")
print(len(orders), len(merged))         # 3 4
print(orders["gmv"].sum(), merged["gmv"].sum())   # 230.0 310.0
```

Order 3 appeared twice, so its 80 was counted twice. Total GMV moved from 230 to 310 with no error.

## Make pandas check for you

```python
try:
    orders.merge(restaurants, on="restaurant_id", how="left", validate="many_to_one")
except pd.errors.MergeError as e:
    print("caught:", e)
```

`validate="many_to_one"` says: each order may match one restaurant, and the restaurants table must have unique keys. If the right side has duplicates, pandas raises `MergeError`. The other options are `"one_to_one"`, `"one_to_many"` and `"many_to_many"`. Using `validate` turns a silent bug into a loud one, and it documents your assumption in code.

The `indicator=True` option adds a `_merge` column that tells you which rows matched:

```python
m = orders.merge(restaurants.drop_duplicates("restaurant_id"),
                 on="restaurant_id", how="left", indicator=True)
print(m["_merge"].value_counts())
```

## Finding and removing duplicates

```python
dup = restaurants.duplicated("restaurant_id", keep=False)
print(restaurants[dup])                              # see them all
unique = restaurants.drop_duplicates("restaurant_id", keep="first")
print(len(unique))
```

`duplicated` marks repeats. With `keep=False` it marks every copy, so you can look at them. `drop_duplicates` keeps the first copy by default. "First" depends on the current row order, so if you need the latest record, sort first:

```python
events = pd.DataFrame({
    "customer_id": [1, 1, 2],
    "updated_at": ["2026-01-02", "2026-01-05", "2026-01-03"],
    "plan": ["free", "pro", "free"],
})
latest = (events.sort_values("updated_at")
                .drop_duplicates("customer_id", keep="last"))
print(latest)
```

## The three traps

**Trap 1: a many-to-many join.** Both sides have repeated keys. If a key appears 3 times on the left and 2 on the right, you get 6 rows for it. The row count grows and no row is exactly wrong, so it is hard to see. Fix: make one side unique first, or aggregate it to one row per key before the merge.

**Trap 2: inner join drops rows silently.** With `how="inner"`, orders whose restaurant is missing from the table vanish. Row count shrinks, and your revenue is too low. Use `how="left"`, then count the rows with a missing right side. Those are orphan keys, and they deserve a line in your answer.

**Trap 3: NaN keys and dtype mismatch.** Pandas matches NaN to NaN in a merge, so rows with a missing key can pair up with each other. And if one side holds the key as an integer and the other as text, you get no matches or an error. Check `dtypes` of both keys and drop or handle null keys first.

## Dropping duplicates is a decision

Before calling `drop_duplicates`, ask: what makes two rows the same thing? A full-row duplicate is usually a double load. Two rows with the same `order_id` but different status are two versions of one order, and you must pick one by a rule such as latest `updated_at`. Say the rule out loud.

## Say it like this

"Before a merge I note the row count and which side should be unique. I use `validate='many_to_one'` so pandas raises if the right table has duplicate keys, and I compare the row count and the sum of the main metric before and after. With a left join I count the rows that found no match, because those are orphan keys. If I need to remove duplicates I sort by the timestamp and keep the last one per key, and I say that this is the rule. A join that changes the row count of the fact table is a bug until proven otherwise."
