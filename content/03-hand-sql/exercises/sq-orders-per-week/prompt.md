Count delivered orders per week. A week is the SQLite string strftime('%Y-%W', created_at), for example '2026-35' (%W: Monday is the first day of the week). Columns: week, orders. Sort by week.

*strftime turns a timestamp text into a label you can GROUP BY.*

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
