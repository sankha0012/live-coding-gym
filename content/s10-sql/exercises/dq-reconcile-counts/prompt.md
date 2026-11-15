Counts from different breakdowns should add up to the same total. Compare the number of rows in `orders` with:

- `by_status`: the sum of the order counts per `status`.
- `by_restaurant`: the sum of the order counts per restaurant, where each order is matched to a row in `restaurants` with an inner join.

- `by_courier`: the sum of the order counts per courier, where each order is matched to a row in `couriers` with an inner join.

Return one row for each of these three checks with `check_name`, `total_orders` (the count of all rows in `orders`), `grouped_total` (the sum for that breakdown) and `difference` (`total_orders - grouped_total`). Sort by `check_name`. A non-zero difference means orders were lost or double counted, or that the join drops rows on purpose (for example, cancelled orders have no courier).

Tables:

```
orders(order_id, customer_id, restaurant_id, courier_id, created_at 'YYYY-MM-DD HH:MM:SS',
       subtotal, delivery_fee, coupon_code, status 'delivered'|'cancelled',
       promised_minutes, actual_minutes)   -- cancelled orders: actual_minutes and courier_id are NULL
restaurants(restaurant_id, name, city, cuisine)
customers(customer_id, name, city, signup_date)
couriers(courier_id, name, vehicle)
```
