Return order_id and subtotal (in that order) of the 23 delivered orders with the highest subtotal. Sort by subtotal from high to low, and break ties by order_id from low to high. Return exactly 23 rows in that order.

Table used:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
