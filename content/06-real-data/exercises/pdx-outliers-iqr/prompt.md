`orders` has `order_id` and `subtotal`. Some subtotals are missing.

Write `iqr_outliers(orders)` that returns the sorted list of `order_id` values whose subtotal is an outlier by the IQR rule.

- Compute Q1 and Q3 of `subtotal` with the pandas default (`Series.quantile`, linear interpolation). Missing values are ignored.
- `IQR = Q3 - Q1`. A value is an outlier when it is below `Q1 - 1.5 * IQR` or above `Q3 + 1.5 * IQR`. A value exactly on a fence is not an outlier.
- Orders with a missing subtotal are never flagged.
- Return a plain Python list of ints, sorted ascending. Return `[]` when nothing is flagged or the data is empty.
- Do not modify the input dataframe.
