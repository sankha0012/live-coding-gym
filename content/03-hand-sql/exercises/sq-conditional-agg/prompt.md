For each restaurant cuisine, return cuisine, delivered (number of delivered orders) and cancelled (number of cancelled orders), in one row per cuisine. Use a single pass over orders, no UNION. Sort by cuisine name.

Tables:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
