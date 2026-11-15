---
title: GROUP BY and aggregate functions
summary: Collapse rows into one row per group and compute COUNT, SUM, AVG, MIN or MAX for each group.
tags: [sql, aggregation]
---
```sql
SELECT courier_id,
       COUNT(*)                      AS orders,
       ROUND(SUM(delivery_fee), 2)   AS fees,
       ROUND(AVG(actual_minutes), 1) AS avg_minutes,
       MAX(created_at)               AS last_order
FROM orders
WHERE status = 'delivered'
GROUP BY courier_id
ORDER BY orders DESC, courier_id;
```

- One output row per different value of the `GROUP BY` columns.
- Every selected column is either in `GROUP BY` or inside an aggregate.
- `WHERE` filters rows before grouping. `HAVING` filters groups after.
- Aggregates skip NULL. Only `COUNT(*)` counts every row.

<!-- more -->

## Details

Clause order: `SELECT ... FROM ... JOIN ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT`.

The aggregate functions are `COUNT(*)`, `COUNT(col)`, `COUNT(DISTINCT col)`, `SUM`, `AVG`, `MIN`, `MAX`. SQLite also has `GROUP_CONCAT(col, ', ')` to glue text values together.

Group by several columns to get one row per combination. You can also group by an expression:

```sql
SELECT strftime('%Y-%m', o.created_at) AS month,
       k.vehicle,
       COUNT(*) AS orders
FROM orders AS o
JOIN couriers AS k ON k.courier_id = o.courier_id
GROUP BY month, k.vehicle
ORDER BY month, k.vehicle;
```

Without `GROUP BY`, an aggregate turns the whole table into one row: `SELECT COUNT(*), AVG(subtotal) FROM orders`. On an empty input `COUNT` gives 0 and the others give NULL.

`AVG` of an integer column returns a decimal in SQLite. `SUM(a) / COUNT(*)` with two integers does integer division, so multiply by `1.0` first.

Dialects: all four dialects accept a `SELECT` alias in `GROUP BY` (like `month` above). SQLite also lets you select a column that is not grouped and not aggregated, and picks a value from some row; Postgres and BigQuery raise an error.

## Common mistakes

- Selecting a column that is not in `GROUP BY`. SQLite returns an arbitrary value with no warning.
- Putting an aggregate in `WHERE` (`WHERE COUNT(*) > 5`). Use `HAVING`.
- Counting rows after a join that repeated them. Use `COUNT(DISTINCT key)`.
- Expecting groups with zero rows to appear. A group exists only if at least one row is in it.

## See also

- [HAVING](#/kb/sql-having)
- [Conditional aggregation (CASE inside SUM, AVG, COUNT)](#/kb/sql-conditional-aggregation)
- [DISTINCT and COUNT(DISTINCT)](#/kb/sql-distinct)
- Official docs: https://www.sqlite.org/lang.html
