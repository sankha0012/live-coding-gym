Return order_id and subtotal (in that order) of delivered orders with a subtotal above 140 that also either used a coupon (coupon_code is not NULL) or had a delivery_fee of 0. Row order does not matter.

Table used:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
