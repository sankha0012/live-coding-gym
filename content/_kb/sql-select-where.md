---
title: SELECT, WHERE and operators
summary: Pick columns with SELECT and keep only the rows that pass the WHERE condition.
tags: [sql, filtering]
---
```sql
SELECT courier_id, name, vehicle
FROM couriers
WHERE vehicle IN ('car', 'bike')
  AND name LIKE 'Courier 0%'
  AND courier_id BETWEEN 1 AND 20;
```

- Text goes in single quotes: `'car'`. Double quotes are for column names.
- `AND` binds tighter than `OR`. Put brackets around every `OR` group.
- `IN (...)` is a list of exact values. `BETWEEN a AND b` includes both ends.
- `LIKE`: `%` is any run of characters, `_` is exactly one character.

<!-- more -->

## Details

`SELECT` lists the output columns. `*` means all columns. Each column can be an expression and can get a name with `AS`:

```sql
SELECT order_id,
       subtotal + delivery_fee AS total,
       ROUND(actual_minutes - promised_minutes, 1) AS delay
FROM orders
WHERE status = 'delivered'
  AND (delivery_fee = 0 OR coupon_code = 'PIZZA20')
  AND created_at >= '2026-10-01' AND created_at < '2026-10-08'
  AND promised_minutes BETWEEN 30 AND 40;
```

Comparison operators: `=`, `<>` (or `!=`), `<`, `<=`, `>`, `>=`. Negations: `NOT IN (...)`, `NOT LIKE`, `NOT BETWEEN`.

Clause order is fixed: `SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT`. The engine runs `WHERE` before `SELECT`, so an alias made in `SELECT` (like `total`) is not safe to use in `WHERE`. Repeat the expression instead.

Dates in this dataset are text like `'2026-10-12 23:37:00'`. Text in that format compares correctly as text. For a whole-day range, use `>=` the first day and `<` the day after the last day.

Dialects: in SQLite and MySQL `LIKE` ignores case for plain letters. In Postgres and BigQuery it is case-sensitive (Postgres has `ILIKE`).

## Common mistakes

- Writing `a = 1 OR b = 2 AND c = 3` and expecting the `OR` to run first. It reads as `a = 1 OR (b = 2 AND c = 3)`.
- Using `= NULL`. It never matches. Use `IS NULL` or `IS NOT NULL`.
- Using `BETWEEN '2026-10-01' AND '2026-10-07'` on a column that has a time part. It drops almost all of the last day.
- Using double quotes for text: `"car"`. SQLite may read it as a column name.

## See also

- [ORDER BY and LIMIT](#/kb/sql-order-limit)
- [NULL: IS NULL, COALESCE, COUNT(col) versus COUNT(*)](#/kb/sql-nulls)
- [Dates in SQLite: strftime, date, julianday](#/kb/sql-dates-sqlite)
- Official docs: https://www.sqlite.org/lang.html
