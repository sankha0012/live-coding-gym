For each status, count the orders three ways. Columns: status, total_orders (all rows), with_coupon (orders where coupon_code is not NULL), with_actual (orders where actual_minutes is not NULL). Sort by status.

An AI assistant wrote the query below. It runs but the result is wrong. Find the bug, fix it by hand, then name it in one sentence.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
