Count delivered orders per day (date of created_at). For the days from 2026-10-20 to 2026-10-31, return day, orders and avg_7d: the average of orders over that day and the 6 rows before it, rounded to 2 decimals. The 6 earlier rows may come from before 2026-10-20, so do not filter days before computing the average. Days with no delivered orders do not appear and are not counted as rows. Sort by day.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
