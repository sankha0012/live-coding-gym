```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, total REAL);

INSERT INTO customers VALUES
  (1, 'Ana',   'Sao Paulo'),
  (2, 'Bruno', 'Recife'),
  (3, 'Carla', 'Sao Paulo'),
  (4, 'Davi',  'Curitiba');
INSERT INTO orders VALUES
  (10, 1, 'delivered', 40.0),
  (11, 1, 'cancelled', 25.0),
  (12, 2, 'delivered', 60.0),
  (13, 3, 'cancelled', 30.0);
```

```sql
SELECT c.name, COUNT(o.id) AS n_delivered
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.status = 'delivered'
GROUP BY c.name
ORDER BY c.name;
```

Explain line by line what this query does, say what it returns for this data, and what goes wrong if the person who wrote it wanted every customer listed, including those with zero delivered orders, and what happens to Carla and Davi.
