```sql
CREATE TABLE deliveries (id INTEGER PRIMARY KEY, courier TEXT, delivered_at TEXT, rating INTEGER);

INSERT INTO deliveries VALUES
  (1, 'Rui', '2026-03-01 12:10', 5),
  (2, 'Rui', '2026-03-01 13:00', NULL),
  (3, 'Rui', NULL,               4),
  (4, 'Lia', '2026-03-02 19:30', 3),
  (5, 'Lia', NULL,               NULL);
```

```sql
SELECT courier,
       COUNT(*)            AS n_rows,
       COUNT(delivered_at) AS n_delivered,
       COUNT(rating)       AS n_rated,
       AVG(rating)         AS avg_rating
FROM deliveries
GROUP BY courier
ORDER BY courier;
```

Explain line by line what this query does, say what it returns for this data, and what goes wrong if a NULL appears in rating or delivered_at, and someone reads avg_rating as the average over all of the courier's rows.
