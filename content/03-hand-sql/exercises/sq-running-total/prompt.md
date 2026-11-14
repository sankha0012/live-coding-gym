For delivered orders created from 2026-10-01 to 2026-10-07 (whole days, inclusive), return one row per day with a delivered order: day (YYYY-MM-DD), revenue (sum of subtotal that day, rounded to 2 decimals) and running_total (sum of revenue from 2026-10-01 up to and including that day, rounded to 2 decimals). Sort by day.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
