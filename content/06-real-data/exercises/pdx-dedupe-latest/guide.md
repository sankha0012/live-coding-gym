**Why this matters.** Tables often keep every version of a record, and you want only the current one. The trap is that "last row in the file" and "latest in time" are not the same thing, because files are rarely sorted by time.

**How we get there.**
1. Order the rows by time: `df.sort_values(time_col, kind="stable")`. Now the newest row of each key sits after all its older rows.
2. Keep one row per key with `drop_duplicates(key, keep="last")`. After the sort, "last" really means "newest".
3. The stable sort matters for ties. Rows with equal times keep their input order, so the later input row ends up last and wins, as the problem asks.
4. Sort by `key` so the output is predictable, then `reset_index(drop=True)` for a fresh `0, 1, 2, ...` index.

None of these steps changes the input, because `sort_values` and `drop_duplicates` return new frames.

**Check it.** An empty frame passes through every step and keeps its columns. The cost is O(n log n), dominated by the sort.

**Watch out.** Calling `drop_duplicates(key, keep="last")` without sorting first keeps the last row in the file, which is only the newest row if the file happens to be in time order.
