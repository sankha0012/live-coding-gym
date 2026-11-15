```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL);

INSERT INTO customers VALUES
  (1, 'Ana'), (2, 'Bruno'), (3, 'Carla'), (4, 'Davi');
INSERT INTO orders VALUES
  (10, 1,    40.0),
  (11, 2,    60.0),
  (12, NULL, 15.0);
```

```sql
SELECT name
FROM customers
WHERE id NOT IN (
  SELECT customer_id
  FROM orders
)
ORDER BY name;
```

Explain line by line what this query does, say what it returns for this data, and what goes wrong if the subquery returns a NULL, as it does here for the order that has no customer_id.
