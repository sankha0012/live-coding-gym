Put every order in a bucket by subtotal: 'unknown' if subtotal is NULL, 'small' if under 42, 'medium' if 42 up to but not including 83, 'large' if 83 or more. Count the orders per bucket. Columns: bucket, orders. Sort by bucket (alphabetical). Check NULL first.

*A CASE returns the first branch that matches.*

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
