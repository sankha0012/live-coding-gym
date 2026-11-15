---
title: ORDER BY and LIMIT
summary: Sort the result with ORDER BY and keep only the first rows with LIMIT.
tags: [sql, sorting]
---
```sql
SELECT order_id, delivery_fee, created_at
FROM orders
ORDER BY delivery_fee DESC, created_at ASC
LIMIT 5;
```

- `ASC` (low to high) is the default. Write `DESC` after each column that needs it.
- Add a tie-breaker column, or rows with equal values come back in any order.
- `LIMIT n` keeps the first `n` rows after sorting. `LIMIT n OFFSET m` skips `m` rows first.

<!-- more -->

## Details

`ORDER BY` and `LIMIT` are the last two clauses of a query, in that order. They run after `WHERE`, `GROUP BY` and `SELECT`, so you can sort by an alias or by an aggregate:

```sql
SELECT courier_id, COUNT(*) AS deliveries
FROM orders
WHERE status = 'delivered'
GROUP BY courier_id
ORDER BY deliveries DESC, courier_id
LIMIT 3 OFFSET 3;
```

This returns places 4 to 6. You can also sort by an expression (`ORDER BY subtotal + delivery_fee DESC`) or by position (`ORDER BY 2 DESC` means the second output column).

Without `ORDER BY` the row order is not defined, even if it looks stable. A `LIMIT` without `ORDER BY` returns arbitrary rows.

NULLs: SQLite and MySQL treat NULL as the smallest value, so NULLs come first with `ASC` and last with `DESC`. Postgres does the opposite. BigQuery sorts NULLs first with `ASC`, like SQLite. To be explicit, SQLite (3.30+), Postgres and BigQuery accept `NULLS FIRST` or `NULLS LAST`:

```sql
SELECT order_id, actual_minutes
FROM orders
ORDER BY actual_minutes ASC NULLS LAST
LIMIT 5;
```

Dialects: `LIMIT` works in SQLite, Postgres, MySQL and BigQuery. SQL Server uses `SELECT TOP 5 ...`.

## Common mistakes

- Writing `ORDER BY a, b DESC` and expecting both to be descending. `DESC` applies only to `b`.
- Leaving out a tie-breaker, so "top 5" changes between runs when values tie.
- Putting `LIMIT` before `ORDER BY`. The order is always `ORDER BY` then `LIMIT`.
- Sorting numbers stored as text: `'10'` sorts before `'9'`.

## See also

- [SELECT, WHERE and operators](#/kb/sql-select-where)
- [ROW_NUMBER, RANK and DENSE_RANK](#/kb/sql-row-number-rank)
- [GROUP BY and aggregate functions](#/kb/sql-group-by)
- Official docs: https://www.sqlite.org/lang.html
