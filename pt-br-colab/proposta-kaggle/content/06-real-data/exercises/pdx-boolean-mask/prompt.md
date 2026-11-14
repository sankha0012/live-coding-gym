Write two functions with pandas.

**1. `flag_orders(df)`**

`df` has the columns `status` (text), `total` (float, can be NaN) and `coupon` (text, can be missing as `None` or NaN). Return a new DataFrame with only the rows where:

- `status` is exactly `"delivered"`, **and**
- either `total` is greater than 100, **or** `coupon` is missing.

Keep the original index and row order. Do not modify `df`.

**2. `count_mismatches(old, new)`**

`old` and `new` are two Series of model predictions with the same index (for example, the live model and a shadow model). Return, as a Python `int`, how many positions are different. Two missing values on the same row count as equal; a missing value against a number counts as different.
