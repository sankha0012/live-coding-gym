List the delivered orders whose `subtotal` is more than twice the average `subtotal` of all delivered orders. Columns: `order_id`, `subtotal`. Sort by `order_id`. Cancelled orders are not part of the average and are not in the result.

*A scalar subquery returns one value you can compare against.*

Table used:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
