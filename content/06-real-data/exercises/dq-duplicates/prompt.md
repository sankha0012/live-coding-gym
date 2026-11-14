Duplicate rows inflate counts and revenue. First, `order_id` is the primary key, so it cannot repeat. In this data there is no repeated `order_id`, so define a duplicate by a business key instead: the same `customer_id`, the same `restaurant_id` and the same calendar date of `created_at` (the first 10 characters, `date(created_at)`).

Return one row per business key that appears more than once: `customer_id`, `restaurant_id`, `order_date` (the date) and `n` (how many orders share the key). Sort by `n` from high to low, then `customer_id`, `restaurant_id`, `order_date`.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
restaurants(restaurant_id, name, city, cuisine)
customers(customer_id, name, city, signup_date)
couriers(courier_id, name, vehicle)
```
