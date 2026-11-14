For each restaurant, find its delivered order(s) with the highest `subtotal`. Columns: `restaurant_id`, `order_id`, `subtotal`. If several delivered orders of a restaurant share the highest subtotal, return all of them. Sort by `restaurant_id`, then `order_id`. Restaurants with no delivered orders do not appear.

*A correlated subquery refers to the current outer row.*

Table used:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
