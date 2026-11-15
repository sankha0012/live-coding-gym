A feed that stopped sending data looks fine until someone checks the dates. Use the fixed reference time `2026-11-01 00:00:00` (do not use the current time). A restaurant is stale when its latest order `created_at` is before `2026-10-29 00:00:00`, which is more than 72 hours before the reference. A restaurant with no orders at all is also stale, with a NULL latest date.

Return `restaurant_id` and `latest_created_at` for each stale restaurant. Sort by `latest_created_at` from oldest to newest, then `restaurant_id`.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
restaurants(restaurant_id, name, city, cuisine)
customers(customer_id, name, city, signup_date)
couriers(courier_id, name, vehicle)
```
