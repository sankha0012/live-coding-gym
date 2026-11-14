List the customers from Rio de Janeiro who have no delivered order. They may have no orders at all, or only cancelled ones. Use NOT EXISTS. Columns: customer_id, name. Sort by customer_id.

Tables:

```
customers(customer_id, name, city, signup_date)
orders(order_id, customer_id, restaurant_id, status 'delivered'|'cancelled')
```
