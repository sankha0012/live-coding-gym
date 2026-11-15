---
title: LEFT JOIN and anti-joins (rows with no match)
summary: LEFT JOIN keeps every left row; filter on a NULL right key or use NOT EXISTS to find rows with no match.
tags: [sql, joins]
---
```sql
-- every courier, with 0 when there is no order from 25 October on
SELECT k.courier_id, k.name, COUNT(o.order_id) AS orders
FROM couriers AS k
LEFT JOIN orders AS o
  ON o.courier_id = k.courier_id AND o.created_at >= '2026-10-25'
GROUP BY k.courier_id, k.name;
-- anti-join: only the couriers with no such order
SELECT k.courier_id, k.name
FROM couriers AS k
LEFT JOIN orders AS o
  ON o.courier_id = k.courier_id AND o.created_at >= '2026-10-25'
WHERE o.order_id IS NULL;
```

- Left rows with no match are kept, with NULL in every right-table column.
- Anti-join: `LEFT JOIN` then `WHERE right_key IS NULL`.
- Count a right-table column, not `*`, so unmatched rows count as 0.

<!-- more -->

## Details

`LEFT JOIN` (same as `LEFT OUTER JOIN`) returns the inner-join rows plus one row for each left row that found no match. The table after `FROM` is the left one, so start from the table whose rows must all stay.

The same anti-join with `NOT EXISTS` reads closer to the question and never repeats rows:

```sql
SELECT k.courier_id, k.name
FROM couriers AS k
WHERE NOT EXISTS (
  SELECT 1 FROM orders AS o
  WHERE o.courier_id = k.courier_id
    AND o.created_at >= '2026-10-25'
);
```

Where you put a filter on the right table matters. In `ON`, it limits which right rows can match, and every left row stays. In `WHERE`, it runs after the join. Unmatched rows have NULL in the right columns, fail the test and are removed, so the query behaves like an inner join. This version loses the couriers with zero orders:

```sql
SELECT k.courier_id, COUNT(o.order_id) AS orders
FROM couriers AS k
LEFT JOIN orders AS o ON o.courier_id = k.courier_id
WHERE o.created_at >= '2026-10-25'
GROUP BY k.courier_id;
```

A filter on the left table (`WHERE k.vehicle = 'car'`) is safe in `WHERE`.

In `NOT EXISTS`, the conditions about the right table go inside the subquery.

Dialects: `LEFT JOIN` and `NOT EXISTS` are the same everywhere. `RIGHT JOIN` and `FULL OUTER JOIN` need SQLite 3.39 or later; MySQL has no `FULL OUTER JOIN`.

## Common mistakes

- Filtering a right-table column in `WHERE`. Unmatched rows have NULL there and are removed.
- Using `COUNT(*)` after a LEFT JOIN. A left row with no match is still one row, so it counts 1.
- Using `NOT IN (SELECT col ...)` when `col` can be NULL. One NULL in the list makes the result empty. Prefer `NOT EXISTS`.
- Testing `IS NULL` on a right column that can be NULL by itself. Test the right table's key.

## See also

- [INNER JOIN](#/kb/sql-joins)
- [Subqueries: scalar, IN, EXISTS, correlated](#/kb/sql-subqueries)
- [NULL: IS NULL, COALESCE, COUNT(col) versus COUNT(*)](#/kb/sql-nulls)
- Official docs: https://www.sqlite.org/lang.html
