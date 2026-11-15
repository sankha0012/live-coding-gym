**Why this matters.** "Orders in the last 7 days" sounds easy, but a rolling window counts rows, not days. If some days have no orders and are missing from the series, a window of 7 rows reaches back further than 7 days and the numbers come out too high.

**How we get there.**
1. An empty input returns an empty integer series with a `DatetimeIndex`, so we stop early.
2. Convert the text with `pd.to_datetime(...)` and round to midnight with `.dt.normalize()`, so every order gets its calendar day.
3. `value_counts().sort_index()` gives the number of orders per day, but only for days that had orders.
4. Build every day with `pd.date_range(first, last, freq="D")` and `reindex(full, fill_value=0)`. Now quiet days exist, with a zero.
5. Only now call `rolling(7, min_periods=1).sum()`. Each row is one day, so 7 rows are 7 days. `min_periods=1` makes the first days sum what exists instead of giving NaN.
6. The sum is a float, so finish with `astype("int64")`.

**Check it.** Counting is linear, and the window pass is linear too.

**Watch out.** Rolling over the sparse daily counts, without reindexing, silently stretches the window across gaps.
