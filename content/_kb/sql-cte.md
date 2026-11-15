---
title: Common table expressions (WITH)
summary: Name a query with WITH so the main query, and later CTEs, can use it like a table.
tags: [sql, cte]
---
```sql
WITH per_courier AS (
  SELECT courier_id, COUNT(*) AS orders
  FROM orders
  WHERE status = 'delivered'
  GROUP BY courier_id
)
SELECT k.vehicle, ROUND(AVG(p.orders), 1) AS avg_orders
FROM per_courier AS p
JOIN couriers AS k ON k.courier_id = p.courier_id
GROUP BY k.vehicle;
```

- `WITH name AS ( query )` comes before the main `SELECT`.
- Write `WITH` once. Separate several CTEs with commas.
- A CTE can read the CTEs defined above it.
- A CTE exists only for this one statement.

<!-- more -->

## Details

A CTE is a named subquery. It does the same job as a subquery in `FROM`, but the steps read top to bottom and one step can be used more than once.

Chain steps by listing them. No comma after the last one:

```sql
WITH daily AS (
  SELECT date(created_at) AS day, COUNT(*) AS orders
  FROM orders
  GROUP BY day
),
stats AS (
  SELECT AVG(orders) AS avg_orders FROM daily
)
SELECT d.day, d.orders
FROM daily AS d
CROSS JOIN stats AS s
WHERE d.orders > 1.5 * s.avg_orders
ORDER BY d.day;
```

Here `daily` is used twice: by `stats` and by the main query. `CROSS JOIN` with a one-row CTE is a simple way to attach a total or an average to every row.

Good habits: one idea per CTE, a name that says what one row is (`per_courier`, `daily`), and only the columns the next step needs. To debug, change the last `SELECT` to `SELECT * FROM daily` and look at one step at a time.

CTEs are the usual way to filter on a window function: compute it in a CTE, filter in the main query.

`WITH RECURSIVE` lets a CTE read itself, for number series or trees. It is rarely needed in interviews.

Dialects: `WITH` works the same in SQLite, Postgres, BigQuery and MySQL 8+. Old MySQL (5.7) has no CTEs.

## Common mistakes

- Writing `WITH` again before the second CTE. It is `WITH a AS (...), b AS (...)`.
- Leaving a comma after the last CTE, before `SELECT`.
- Using a CTE before it is defined. Order matters.
- Forgetting to name a computed column with `AS`, then not being able to refer to it.
- Ending a CTE with a semicolon. The whole statement has one semicolon, at the end.

## See also

- [Subqueries: scalar, IN, EXISTS, correlated](#/kb/sql-subqueries)
- [Window functions: OVER, PARTITION BY, ORDER BY](#/kb/sql-window-functions)
- [De-duplicating rows](#/kb/sql-dedupe)
- Official docs: https://www.sqlite.org/lang.html
