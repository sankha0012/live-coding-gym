For each customer who lives in Curitiba and has at least two delivered orders, return their second most recent delivered order. Columns: customer_id, order_id, created_at, subtotal. If two orders of a customer have the same created_at, the one with the higher order_id counts as more recent. Customers with only one delivered order do not appear. Sort by customer_id.

Tables:

```
customers(customer_id, name, city, signup_date)
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
