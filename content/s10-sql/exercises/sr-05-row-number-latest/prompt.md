```sql
CREATE TABLE courier_status (id INTEGER PRIMARY KEY, courier_id INTEGER, status TEXT, updated_at TEXT);

INSERT INTO courier_status VALUES
  (1, 1, 'offline', '2026-03-01 08:00'),
  (2, 1, 'online',  '2026-03-01 09:30'),
  (3, 1, 'busy',    '2026-03-01 09:30'),
  (4, 2, 'online',  '2026-03-01 07:45'),
  (5, 2, 'offline', '2026-03-01 18:00');
```

```sql
SELECT courier_id, status, updated_at
FROM (
  SELECT courier_id, status, updated_at,
         ROW_NUMBER() OVER (
           PARTITION BY courier_id
           ORDER BY updated_at DESC
         ) AS rn
  FROM courier_status
)
WHERE rn = 1
ORDER BY courier_id;
```

Explain line by line what this query does, say what it returns for this data, and what goes wrong if two status rows for the same courier have the same updated_at.
