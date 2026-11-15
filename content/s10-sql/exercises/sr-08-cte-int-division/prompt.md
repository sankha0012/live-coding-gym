```sql
CREATE TABLE orders (id INTEGER PRIMARY KEY, city TEXT, status TEXT);

INSERT INTO orders VALUES
  (1, 'Recife',   'delivered'),
  (2, 'Recife',   'delivered'),
  (3, 'Recife',   'cancelled'),
  (4, 'Natal',    'delivered'),
  (5, 'Natal',    'cancelled'),
  (6, 'Natal',    'cancelled'),
  (7, 'Natal',    'cancelled'),
  (8, 'Salvador', 'delivered');
```

```sql
WITH per_city AS (
  SELECT city, COUNT(*) AS n_orders,
         SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS n_cancelled
  FROM orders
  GROUP BY city
),
rates AS (
  SELECT city, n_cancelled / n_orders AS cancel_rate
  FROM per_city
)
SELECT city, cancel_rate
FROM rates
WHERE cancel_rate >= 0.3
ORDER BY city;
```

Explain line by line what this query does, say what it returns for this data, and what goes wrong if both operands of the division are integers, which is what COUNT and a SUM of 1s and 0s produce.
