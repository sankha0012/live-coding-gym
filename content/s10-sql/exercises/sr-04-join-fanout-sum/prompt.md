```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL);
CREATE TABLE order_items (id INTEGER PRIMARY KEY, order_id INTEGER, sku TEXT);

INSERT INTO orders VALUES
  (1, 100, 50.0),
  (2, 100, 30.0),
  (3, 101, 20.0);
INSERT INTO order_items VALUES
  (1, 1, 'pizza'),
  (2, 1, 'soda'),
  (3, 1, 'dessert'),
  (4, 2, 'burger'),
  (5, 3, 'salad'),
  (6, 3, 'juice');
```

```sql
SELECT o.customer_id, SUM(o.total) AS revenue
FROM orders o
JOIN order_items i ON i.order_id = o.id
GROUP BY o.customer_id
ORDER BY o.customer_id;
```

Explain line by line what this query does, say what it returns for this data, and what goes wrong if an order has several items, which is the normal case here, and someone trusts the revenue column as the customer's real spend.
