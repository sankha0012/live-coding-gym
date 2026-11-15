# Joins that multiply rows

## What it is

A join should add columns to a fact table, such as the city of each order. It must not change how many orders you have. When the lookup side has repeated keys, each match creates another row. See [merge](#/kb/pd-merge).

## How it breaks in production

- **Fan-out.** One restaurant listed twice makes every one of its orders appear twice. Nothing crashes, and revenue is silently too high.
- **Many-to-many.** A key repeated 3 times on the left and 2 on the right gives 6 rows.
- **Inner join drops rows.** Orders whose restaurant is missing from the table vanish, and the totals are too low.
- **Null and mismatched keys.** pandas matches `NaN` keys to each other, and an integer key against a text key matches nothing.

## The defence in code

```python
import pandas as pd

orders = pd.DataFrame({"order_id": [1, 2, 3, 4],
                       "restaurant_id": [10, 10, 20, 99],
                       "gmv": [100.0, 50.0, 80.0, 10.0]})
rest = pd.DataFrame({"restaurant_id": [10, 20, 20], "city": ["SP", "RJ", "RJ"]})

bad = orders.merge(rest, on="restaurant_id", how="left")
print(len(bad), bad["gmv"].sum())            # 5 320.0, should be 4 and 240.0

try:
    orders.merge(rest, on="restaurant_id", how="left", validate="many_to_one")
except pd.errors.MergeError as e:
    print("caught")

def add_city(orders, rest):
    out = orders.merge(rest.drop_duplicates("restaurant_id"), on="restaurant_id",
                       how="left", validate="many_to_one", indicator=True)
    assert len(out) == len(orders), "join changed the row count"
    return out

out = add_city(orders, rest)
print(out["_merge"].value_counts().to_dict())
```

The naive left join returns 5 rows and a GMV of 320 instead of 240, with no error. `validate="many_to_one"` turns that into a `MergeError`. In the function I deduplicate the lookup, keep a left join so no order is lost, assert the row count, and use `indicator=True` to count orders with no restaurant: here 1 is `left_only` and 3 are `both`. Those orphan keys deserve a line in the answer.

## What to say in the interview

"Before a merge I write down the row count and which side must be unique. I pass `validate='many_to_one'` so pandas raises if the lookup has duplicate keys, and I assert that the row count is unchanged. I use a left join and count the unmatched rows, because an inner join hides them. A join that changes the size of the fact table is a bug until proven otherwise."
