---
title: HAVING
summary: Filter groups after GROUP BY using a condition on an aggregate.
tags: [sql, aggregation]
---
```sql
SELECT courier_id, COUNT(*) AS orders
FROM orders
WHERE status = 'delivered'      -- filters rows, before grouping
GROUP BY courier_id
HAVING COUNT(*) >= 25           -- filters groups, after grouping
ORDER BY orders DESC, courier_id;
```

- `WHERE` cannot contain an aggregate. `HAVING` can.
- `HAVING` comes after `GROUP BY` and before `ORDER BY`.
- The aggregate in `HAVING` does not need to be in the `SELECT` list.

<!-- more -->

## Details

The engine works in this order: `FROM` and joins, `WHERE`, `GROUP BY`, aggregates, `HAVING`, `SELECT`, `ORDER BY`, `LIMIT`. So `WHERE` decides which rows enter the groups, and `HAVING` decides which finished groups stay.

You can combine several conditions with `AND` and `OR`, and use any aggregate:

```sql
SELECT customer_id,
       COUNT(*) AS orders,
       ROUND(AVG(subtotal), 2) AS avg_subtotal
FROM orders
GROUP BY customer_id
HAVING COUNT(*) >= 5
   AND AVG(subtotal) > 110
   AND COUNT(DISTINCT restaurant_id) >= 4
ORDER BY customer_id;
```

Put a condition in `WHERE` when it is about single rows (a status, a date). It is faster and clearer. Put it in `HAVING` only when it needs the aggregate.

A common use is finding duplicates: group by the key and keep groups with `HAVING COUNT(*) > 1`.

`HAVING` with no `GROUP BY` treats the whole table as one group. This is rare.

Dialects: SQLite, MySQL and BigQuery accept a `SELECT` alias in `HAVING` (`HAVING orders >= 25`). Postgres does not, so repeating the aggregate is the portable form.

## Common mistakes

- Writing `WHERE COUNT(*) > 5`. This is an error ("misuse of aggregate"). Move it to `HAVING`.
- Putting a row filter in `HAVING` (`HAVING status = 'delivered'`). In SQLite it runs on an arbitrary row of each group and gives wrong results.
- Placing `HAVING` before `GROUP BY` or after `ORDER BY`.
- Filtering in `HAVING` when the question is about rows inside the group. "Customers with 5 delivered orders" needs `WHERE status = 'delivered'` first, then `HAVING COUNT(*) >= 5`.

## See also

- [GROUP BY and aggregate functions](#/kb/sql-group-by)
- [SELECT, WHERE and operators](#/kb/sql-select-where)
- [Data-quality queries: nulls, duplicates, orphans, ranges](#/kb/sql-data-quality-checks)
- Official docs: https://www.sqlite.org/lang.html
