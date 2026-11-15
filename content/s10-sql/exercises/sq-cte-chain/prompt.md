Compute each restaurant's revenue (sum of `subtotal` of delivered orders), then each city's total revenue (the sum of its restaurants' revenue). Return the restaurants whose revenue is more than 20 percent of their city's total. Columns: `restaurant_id`, `city`, `share`, where `share` is revenue divided by city total, rounded to 3 decimals. Sort by `city`, then `restaurant_id`. Use the `city` of the restaurant, not of the customer.

*Chain two CTEs: the second one reads the first.*

Tables used:

```
restaurants(restaurant_id, name, city, cuisine)
orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee,
       coupon_code, status 'delivered'|'cancelled', promised_minutes, actual_minutes)
```
