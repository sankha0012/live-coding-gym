For each cuisine, return the number of delivered orders and the total subtotal of those orders, rounded to 2 decimals. Columns: cuisine, orders, revenue. Sort by revenue descending, then cuisine.

An AI assistant wrote the query below. It runs but the result is wrong. Find the bug, fix it by hand, then name it in one sentence.

Tables:

```
orders(order_id, restaurant_id, subtotal, status)
restaurants(restaurant_id, name, city, cuisine)
```
