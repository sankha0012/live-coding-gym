Find customers who ordered from the same burger restaurant in Rio de Janeiro at least twice (any status). Columns: customer_id, restaurant_id, one row per customer and restaurant pair, no duplicates. Sort by customer_id, then restaurant_id.

*Join orders to itself.*

Tables:

```
orders(order_id, customer_id, restaurant_id, status)
restaurants(restaurant_id, name, city, cuisine)
```
