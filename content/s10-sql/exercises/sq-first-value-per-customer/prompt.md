For customers 22, 117 and 179, list every delivered order that has a subtotal (not NULL). Columns: customer_id, order_id, subtotal, first_subtotal (the subtotal of that customer's earliest such order) and diff (subtotal minus first_subtotal, rounded to 2 decimals). The earliest order is the one with the lowest created_at, ties by order_id. Sort by customer_id, created_at, order_id.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
