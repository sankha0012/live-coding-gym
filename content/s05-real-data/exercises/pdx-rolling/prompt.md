`orders` has `created_at` as text like `2026-10-12 23:37:00`.

Write `rolling_7d_orders(orders)` that returns a pandas Series with the number of orders in the last 7 days, for every calendar day.

- Daily count: orders per calendar day (the date part of `created_at`).
- The index is a daily `DatetimeIndex` (midnight timestamps) with every day from the first order day to the last order day. A day with no orders has a daily count of 0.
- The value on day `D` is the sum of the daily counts for `D` and the 6 days before it (7 days in total). On the first days there are fewer than 7 days of data: sum what exists, never return NaN.
- Values are integers. Return an empty Series for an empty `orders`.
- Do not modify the input dataframe.
