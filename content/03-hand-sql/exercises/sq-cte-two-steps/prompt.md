Compute the revenue of each restaurant: the sum of `subtotal` over its delivered orders, rounded to 2 decimals. Return the restaurants whose revenue is greater than the average revenue across restaurants (average over restaurants that have at least one delivered order). Columns: `restaurant_id`, `revenue`. Sort by `revenue` descending, then `restaurant_id`.

*Name step one in a CTE, then use it twice.*

Table used:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
