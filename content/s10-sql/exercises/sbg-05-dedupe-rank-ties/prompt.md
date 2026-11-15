For customers with customer_id 1 to 5, keep only the most recent order for each (customer_id, restaurant_id) pair. Most recent means the highest created_at; if created_at ties, the higher order_id wins. Columns: order_id, customer_id, restaurant_id. Sort by customer_id, restaurant_id.

An AI assistant wrote the query below. It runs but the result is wrong. Find the bug, fix it by hand, then name it in one sentence.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
