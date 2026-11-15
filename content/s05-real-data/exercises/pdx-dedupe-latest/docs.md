## Contract

`latest_per_key(df: pd.DataFrame, key: str, time_col: str) -> pd.DataFrame`

`df` has several versions of each record. `key` and `time_col` are column names.

- The result has exactly one row per distinct value of `key`: the row with the largest `time_col`.
- If two rows of one key share the maximum time, the one that appears later in the input wins.
- The whole winning row is kept as it is, including missing values. Do not fill gaps from older versions.
- All original columns are kept in their original order.
- Rows are sorted by `key` ascending, and the index is `0, 1, 2, ...`.
- The input frame is not modified.
- An empty frame returns an empty frame with the same columns.

Example: rows `(1, 10:00, "a")`, `(1, 11:00, "b")`, `(2, 09:00, "c")` give `(1, 11:00, "b")` and `(2, 09:00, "c")`.

## Library notes

- `DataFrame.sort_values(by, kind="quicksort")` returns a new frame. Only `kind="stable"` (or `"mergesort"`) guarantees that equal values keep their input order.
- `DataFrame.drop_duplicates(subset=None, keep="first")` returns a new frame and keeps the first or last occurrence in the current row order. `keep=False` drops all copies.
- `DataFrame.reset_index(drop=True)` returns a new frame with a fresh `0..n-1` index; without `drop=True` the old index becomes a column.
- `SeriesGroupBy.idxmax()` returns the index label of the first maximum in each group, so on ties it picks the earlier row.

## Gotchas

- Row order in a file is not time order. Late-arriving events are common in production, so the last row is not necessarily the newest version.
- Tie-breaking rules must be explicit, otherwise two runs on the same data can pick different rows.
- Taking the max of each column separately builds a record that never existed. Select whole rows.
