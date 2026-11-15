List the customers from Curitiba who have never placed any order (of any status). Columns: customer_id, name. Sort by customer_id.

*LEFT JOIN, then keep the rows with no match.*

Tables:

```
customers(customer_id, name, city, signup_date)
orders(order_id, customer_id, restaurant_id, status)
```
