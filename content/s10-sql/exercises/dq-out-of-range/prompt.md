Check `orders` for impossible or suspicious values. Return one row per rule with `rule_name` and `violations` (the number of orders that break it). Always return all four rows, even when the count is 0. Sort by `rule_name`.

- `actual_over_4x`: `actual_minutes` is above 4 times `promised_minutes`. NULL does not count.
- `negative_amount`: `subtotal` or `delivery_fee` is below 0. NULL does not count.
- `nonpositive_minutes`: `promised_minutes` is 0 or less, or `actual_minutes` is below 0.
- `subtotal_over_150`: `subtotal` is above 150.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
restaurants(restaurant_id, name, city, cuisine)
customers(customer_id, name, city, signup_date)
couriers(courier_id, name, vehicle)
```
