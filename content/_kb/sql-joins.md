---
title: INNER JOIN
summary: Combine rows from two tables where a key matches; rows with no match are dropped.
tags: [sql, joins]
---
```sql
SELECT o.order_id, k.name AS courier_name, k.vehicle
FROM orders AS o
JOIN couriers AS k ON k.courier_id = o.courier_id
WHERE o.created_at >= '2026-10-31'
ORDER BY o.order_id;
```

- `JOIN` alone means `INNER JOIN`.
- `ON` says which columns must match. Only matching pairs of rows are kept.
- Give each table a short alias and prefix every column: `o.order_id`.

<!-- more -->

## Details

For each row of the left table, the join finds every row of the right table that passes the `ON` condition. No match means the row disappears. Here, cancelled orders have a NULL `courier_id`, so they are not in the result. NULL never equals anything.

Add more tables by adding more `JOIN ... ON ...` lines. `JOIN` comes after `FROM` and before `WHERE`:

```sql
SELECT r.cuisine, k.vehicle, COUNT(*) AS orders
FROM orders AS o
JOIN restaurants AS r ON r.restaurant_id = o.restaurant_id
JOIN couriers    AS k ON k.courier_id    = o.courier_id
WHERE r.city = 'Curitiba'
GROUP BY r.cuisine, k.vehicle
ORDER BY r.cuisine, k.vehicle;
```

Row counts: joining orders to restaurants keeps one row per order, because each order has one restaurant (many-to-one). Joining restaurants to orders repeats each restaurant once per order (one-to-many). Know which side is "many" before you count or sum.

When both tables use the same column name, `USING` is a shorter form: `JOIN couriers USING (courier_id)`.

Dialects: `JOIN ... ON` is the same in SQLite, Postgres, MySQL and BigQuery. `USING` is supported by all four.

## Common mistakes

- Forgetting the `ON` clause. SQLite then pairs every row with every row (a cross join) with no error.
- Selecting `name` when two joined tables have a `name` column. This is an "ambiguous column" error; write `k.name`.
- Summing a column from the "one" side after joining to the "many" side. The value is repeated and the sum is too large.
- Expecting rows with no match to appear. Use a LEFT JOIN for that.

## See also

- [LEFT JOIN and anti-joins (rows with no match)](#/kb/sql-left-join-anti-join)
- [Self joins](#/kb/sql-self-join)
- [GROUP BY and aggregate functions](#/kb/sql-group-by)
- Official docs: https://www.sqlite.org/lang.html
