## Contract

`fill_subtotal(orders: pd.DataFrame) -> pd.DataFrame`

`orders` has columns `order_id`, `restaurant_id` and `subtotal` (float, some values NaN), plus possibly others.

- Returns a copy in which every missing `subtotal` is replaced by the median `subtotal` of the same `restaurant_id`. Medians ignore missing values.
- If a restaurant has no known subtotal at all, the median of the whole `subtotal` column is used for it.
- Known subtotals and all other columns are unchanged.
- Row order and index are kept, including a non-default index.
- The input frame is not modified.
- An empty frame, or a frame with nothing missing, comes back unchanged.

Example: restaurant 1 has subtotals 10, NaN, 30 and restaurant 3 has only NaN, while the column holds 10, 30, 100, 50 as known values. The NaN of restaurant 1 becomes 20 and the NaN of restaurant 3 becomes 40.

## Library notes

- `Series.median(skipna=True)` returns a float and ignores NaN. On an all-NaN or empty Series it returns NaN.
- `SeriesGroupBy.transform("median")` returns a Series aligned to the original index, with each row holding its group's median. A group with no known values gives NaN.
- `Series.fillna(value)` returns a new Series. `value` can be a scalar or a Series, which is matched by index label.
- `DataFrame.copy()` returns a deep copy by default; assigning a column on the original changes the caller's data.

## Gotchas

- A global median hides differences between groups, and a per-group median can be unstable for small groups. Always have a fallback for groups with no data.
- Imputing with a statistic computed on the full dataset before a train/test split leaks test information into training.
- Imputed values should be traceable in production. Silent filling can hide an upstream data outage.
