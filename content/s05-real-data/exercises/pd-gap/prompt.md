`orders` has `customer_id` and `created_at`. The `created_at` column is read from the CSV as text, so convert it to datetime first.

Write `days_since_previous(orders)` that returns, for each order, how many days have passed since the same customer's previous order.

- Return a pandas Series with the same index as `orders` (one value per row, any row order is fine). Values are floats, in days, for example 1.5 for 36 hours.
- Previous means the earlier `created_at` of the same `customer_id`, whatever the status.
- A customer's first order has no previous order, so its value is NaN.
- `orders` may come in any row order. Do not modify the input dataframe.
