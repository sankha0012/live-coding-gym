`orders` has `subtotal` (some values are missing), `delivery_fee` and `status`. `restaurants` has `restaurant_id` and `city`.

Write `gmv_by_city(orders, restaurants)` that returns the GMV of delivered orders by city, largest first.

- Only orders with `status == "delivered"` count.
- GMV of one order is `subtotal + delivery_fee`. A missing subtotal counts as 0.
- Return a pandas Series indexed by `city`, sorted from largest to smallest GMV.
- Do not modify the input dataframes. Every order's `restaurant_id` exists in `restaurants`.
