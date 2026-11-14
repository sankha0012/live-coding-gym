An orphan is a row that points to something that does not exist. Run four checks on `orders` and return one row per check with `check_name` and `problem_count`:

- `delivered_without_courier`: orders with status `delivered` and a NULL `courier_id`.
- `missing_courier`: orders whose `courier_id` is NOT NULL but has no match in `couriers`. A NULL `courier_id` on its own is not an orphan.
- `missing_customer`: orders whose `customer_id` has no match in `customers`.
- `missing_restaurant`: orders whose `restaurant_id` has no match in `restaurants`.

Always return all four rows, even when the count is 0. Sort by `check_name`.

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
restaurants(restaurant_id, name, city, cuisine)
customers(customer_id, name, city, signup_date)
couriers(courier_id, name, vehicle)
```
