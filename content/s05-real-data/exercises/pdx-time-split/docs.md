## Contract

`time_split(orders: pd.DataFrame, cutoff: str) -> tuple[pd.DataFrame, pd.DataFrame]`

`orders` has `created_at` stored as text such as `"2026-10-12 23:37:00"`. `cutoff` is a date string such as `"2026-10-01"`, meaning midnight at the start of that day.

- Returns `(train, test)`.
- `train` holds the orders with `created_at` strictly before the cutoff.
- `test` holds the orders at the cutoff or later. A row at exactly `2026-10-01 00:00:00` goes to `test`; `2026-09-30 23:59:59` goes to `train`.
- Each row is in exactly one side. Nothing is lost and nothing overlaps.
- Row order and all columns are kept. `created_at` stays as text in both outputs.
- The input is not modified. An empty side is returned as an empty frame with the same columns.

## Library notes

- `pd.to_datetime(arg, errors="raise")` converts text to `datetime64` and returns a Series for a Series input. Unparseable text raises, or becomes `NaT` with `errors="coerce"`.
- A datetime Series can be compared with a date string using `<` and `>=`. The string is parsed as midnight of that day. The result is a boolean Series.
- `df[mask]` and `df.loc[mask]` return a new frame with the rows where the mask is `True`, in the original order and with the original index.
- `~mask` inverts a boolean Series. A comparison with `NaT` is always `False`, so a `NaT` row is in neither `<` nor `>=` and would be lost.

## Gotchas

- Splitting by time instead of randomly is what stops a model from learning from the future. Shuffling before splitting leaks information.
- Comparing text with text works only while the format is perfectly consistent. Parse timestamps before comparing.
- Writing the parsed dates back into the frame changes the data the caller gave you. Parse into a temporary Series.
