```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, restaurant_id INTEGER, status TEXT, total REAL);

INSERT INTO orders VALUES
  (1, 7, 'delivered', 50),
  (2, 7, 'delivered', 70),
  (3, 7, 'cancelled', 20),
  (4, 8, 'delivered', 30),
  (5, 8, 'cancelled', 45),
  (6, 9, 'delivered', 90),
  (7, 9, 'delivered', 10),
  (8, 9, 'delivered', 40);
```

```sql
SELECT restaurant_id, COUNT(*) AS n_orders, SUM(total) AS revenue
FROM orders
WHERE status = 'delivered'
GROUP BY restaurant_id
HAVING COUNT(*) >= 2 AND SUM(total) > 80
ORDER BY revenue DESC;
```

Explain line by line what this query does, say what it returns for this data, and what goes wrong if the status filter is moved from WHERE into HAVING, or the HAVING threshold uses a row-level column such as total instead of an aggregate.
