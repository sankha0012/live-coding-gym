For customers who live in Curitiba and have at least one delivered order, compute spend (sum of subtotal of delivered orders, rounded to 2 decimals). Split these customers into 4 bands with NTILE(4), band 1 for the highest spend. Order for the split: spend descending, then customer_id ascending. Return customer_id, spend, band. Sort by band, then spend descending, then customer_id.

Tables:

```
customers(customer_id, name, city, signup_date)
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
