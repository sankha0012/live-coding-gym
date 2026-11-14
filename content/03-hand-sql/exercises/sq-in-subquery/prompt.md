List the customers who have at least 3 cancelled orders. Columns: `customer_id`, `name`. Sort by `customer_id`. Use `IN` with a subquery on `orders`.

*IN (subquery) tests membership in a list built by another query.*

Tables used:

```
customers(customer_id, name, city, signup_date)
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
