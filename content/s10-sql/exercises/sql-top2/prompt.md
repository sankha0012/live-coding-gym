The 2 restaurants with the highest revenue (sum of subtotal of delivered orders) in each city. Columns: city, restaurant_id, revenue, rn. Sort by city and rn.

*ROW_NUMBER over a partition.*

Tables:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
