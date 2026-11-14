For customer 3, list each delivered order with the time of the customer's next delivered order. Columns: order_id, created_at, next_created_at, days_to_next (days between the two, rounded to 1 decimal). The last order has NULL in both next columns. Orders are ordered by created_at, ties by order_id. Sort the result the same way.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
