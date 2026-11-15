For each restaurant cuisine, return cuisine and avg_subtotal: the average subtotal of delivered orders, rounded to 2 decimals. Some orders have no subtotal (NULL): leave them out of the average, do not count them as 0. Sort by cuisine name.

Tables:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
