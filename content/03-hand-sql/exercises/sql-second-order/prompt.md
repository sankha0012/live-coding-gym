Among customers with at least 2 delivered orders, what is the average number of days between the 1st and 2nd order? One row, one column.

*ROW_NUMBER + self join.*

Tables:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
```
