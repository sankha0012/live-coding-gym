`orders` has `restaurant_id`, `status`, `promised_minutes` and `actual_minutes`. `restaurants` has `restaurant_id` and `city`. Merge them to get each order's city, then build one table by city for delivered orders.

Write `city_dashboard(orders, restaurants)` that returns a DataFrame indexed by `city` with these columns:

- `orders`: number of delivered orders.
- `late_rate`: share of delivered orders that are late, a fraction from 0 to 1. An order is late when `actual_minutes > promised_minutes`.
- `avg_late`: average minutes late among the late orders only, where minutes late is `actual_minutes - promised_minutes`. If a city has no late orders this is NaN.

Only orders with `status == "delivered"` count. Do not modify the input dataframes. Row order does not matter. Every order's `restaurant_id` exists in `restaurants`.
