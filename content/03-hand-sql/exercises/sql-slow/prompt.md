Restaurants with at least 40 delivered orders and an average actual time above 42 minutes. Show restaurant_id, n and avg_min, slowest first.

*WHERE vs HAVING.*

Tables:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
