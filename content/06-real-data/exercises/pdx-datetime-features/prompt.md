Write `add_time_features(orders: pd.DataFrame) -> pd.DataFrame`. The column `created_at` holds text such as `"2026-10-12 23:37:00"`.

Return a copy of `orders` with three new columns, built from `created_at`:

- `hour`: the hour of the day as an integer from 0 to 23.
- `weekday`: the day of the week as an integer, Monday is 0 and Sunday is 6.
- `is_weekend`: `True` for Saturday and Sunday, otherwise `False`.

All original columns stay unchanged (`created_at` stays text). Do not modify the input. The frame can have zero rows.
