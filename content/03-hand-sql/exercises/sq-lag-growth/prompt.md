For delivered orders, compute revenue per restaurant city and month (city from the restaurant, month as 'YYYY-MM', revenue = sum of subtotal; NULL subtotals are ignored by SUM). Return city, month, revenue (rounded to 2 decimals) and growth_pct: the percent change from the previous month of the same city, rounded to 1 decimal. A city's first month has growth_pct NULL. Sort by city, then month.

Tables:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
