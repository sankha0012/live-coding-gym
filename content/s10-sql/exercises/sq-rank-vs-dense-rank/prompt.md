Count the delivered orders of each restaurant. Return restaurant_id, orders, rnk (RANK by orders, highest first) and drnk (DENSE_RANK by the same rule). Restaurants with the same count share the same rank. Include only restaurants with at least one delivered order. Sort by rnk, then restaurant_id.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
