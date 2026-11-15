Add an optional fourth parameter `earliest`, default `False`. When it is `True`, keep for each key the row with the SMALLEST value in `time_col` instead of the largest. If two rows of the same key tie on that smallest time, keep the one that appears EARLIER in the input. The result is still sorted by `key` with a fresh index, and the input is not modified. With the default, nothing changes.

Example: rows `(1, 10:00, "a")`, `(1, 11:00, "b")`, `(2, 09:00, "c")` with `earliest=True` give `(1, 10:00, "a")` and `(2, 09:00, "c")`.
