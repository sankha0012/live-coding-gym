```sql
CREATE TABLE payments (id INTEGER PRIMARY KEY, store TEXT, paid_on TEXT, amount INTEGER);

INSERT INTO payments VALUES
  (1, 'A', '2026-03-01', 10),
  (2, 'A', '2026-03-02', 20),
  (3, 'A', '2026-03-02',  5),
  (4, 'B', '2026-03-01',  7),
  (5, 'B', '2026-03-03',  3);
```

```sql
SELECT store, paid_on, amount,
       SUM(amount) OVER (
         PARTITION BY store
         ORDER BY paid_on
       ) AS running
FROM payments
ORDER BY store, paid_on, id;
```

Explain line by line what this query does, say what it returns for this data, and what goes wrong if two payments of the same store share the same paid_on date.
