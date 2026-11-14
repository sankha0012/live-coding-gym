Before trusting a table, check how much of it is missing. For the `orders` table, report the null rate of these columns: `subtotal`, `courier_id`, `coupon_code`, `actual_minutes`. The null rate is the number of NULL values divided by the number of orders, times 100, rounded to 2 decimals.

Return `column_name` and `null_pct`, but only for columns that have at least one NULL. Sort by `null_pct` from high to low, ties by `column_name`.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
restaurants(restaurant_id, name, city, cuisine)
customers(customer_id, name, city, signup_date)
couriers(courier_id, name, vehicle)
```
