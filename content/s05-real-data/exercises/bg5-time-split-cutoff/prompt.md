`orders` has `created_at` as text like `2026-10-12 23:37:00`.

Write `time_split(orders, cutoff)` that returns `(train, test)` for a model that must predict the future.

- `cutoff` is a string such as `"2026-10-01"`, meaning midnight at the start of that day.
- `train` holds the orders created strictly before the cutoff. `test` holds the orders created at the cutoff or later.
- Every order is in exactly one of the two, so there is no overlap and nothing is lost.
- Do not shuffle or sort. Keep the original row order and all original columns. Leave `created_at` as it came.
- Do not modify the input dataframe. An empty side is allowed and is returned as an empty dataframe.

An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
