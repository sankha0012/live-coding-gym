A table has several versions of the same record. Write `latest_per_key(df: pd.DataFrame, key: str, time_col: str) -> pd.DataFrame`.

It keeps exactly one row for each value of the column `key`: the row with the largest value in `time_col`. If two rows of the same key have the same time, keep the one that appears later in the input.

The result has all the original columns, is sorted by `key` ascending, and has a fresh index `0, 1, 2, ...`. Do not modify the input. An empty frame returns an empty frame with the same columns.

Example: rows `(1, 10:00, "a")`, `(1, 11:00, "b")`, `(2, 09:00, "c")` with key `id` give `(1, 11:00, "b")` and `(2, 09:00, "c")`.

An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
