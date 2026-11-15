---
title: Conditional aggregation (CASE inside SUM, AVG, COUNT)
summary: Put a CASE inside an aggregate to count or sum only the rows that meet a condition, in one pass.
tags: [sql, aggregation]
---
```sql
SELECT k.vehicle,
       COUNT(*) AS orders,
       SUM(CASE WHEN o.actual_minutes <= 30 THEN 1 ELSE 0 END) AS fast,
       ROUND(AVG(CASE WHEN o.actual_minutes <= 30 THEN 1.0 ELSE 0 END), 3) AS fast_rate,
       ROUND(SUM(CASE WHEN o.delivery_fee = 0 THEN o.subtotal END), 2) AS free_fee_sales
FROM orders AS o
JOIN couriers AS k ON k.courier_id = o.courier_id
GROUP BY k.vehicle;
```

- `SUM(CASE WHEN cond THEN 1 ELSE 0 END)` counts the rows where `cond` is true.
- `AVG(CASE WHEN cond THEN 1.0 ELSE 0 END)` gives the share of rows (0 to 1).
- `SUM(CASE WHEN cond THEN col END)` sums `col` only for those rows.

<!-- more -->

## Details

The `CASE` runs once per row and returns a number or NULL. The aggregate then works on those values. This lets one `GROUP BY` produce several filtered numbers side by side, instead of one query per filter.

There are three ways to count matching rows. They give the same result:

```sql
SELECT status,
       SUM(CASE WHEN coupon_code = 'PIZZA20' THEN 1 ELSE 0 END) AS a,
       COUNT(CASE WHEN coupon_code = 'PIZZA20' THEN 1 END)      AS b,
       COUNT(*) FILTER (WHERE coupon_code = 'PIZZA20')          AS c
FROM orders
GROUP BY status;
```

`COUNT(CASE ... END)` has no `ELSE`, so rows that do not match become NULL, and `COUNT` skips NULL. With `ELSE 0` it would count every row.

A row where the condition is NULL (for example `actual_minutes` is NULL) goes to `ELSE`. For a rate, decide if those rows belong in the denominator. To leave them out, filter them in `WHERE`, or return NULL for them so `AVG` skips them.

This is also how you pivot: one `SUM(CASE ...)` column per category.

Dialects: `CASE` inside an aggregate works everywhere. `FILTER (WHERE ...)` works in SQLite 3.30+ and Postgres, not in MySQL or BigQuery. BigQuery has `COUNTIF(cond)`. In SQLite and MySQL a comparison is 0 or 1, so `SUM(status = 'cancelled')` also works; Postgres needs the `CASE`.

## Common mistakes

- Writing `COUNT(CASE WHEN cond THEN 1 ELSE 0 END)`. It counts every row, because 0 is not NULL.
- Computing a rate as `SUM(...) / COUNT(*)` with two integers. Integer division drops the decimals; multiply by `1.0` first.
- Forgetting `ELSE 0` in a `SUM`. If no row matches, the result is NULL, not 0.
- Putting the condition in `WHERE`. That removes the rows for every other column too.

## See also

- [CASE expressions](#/kb/sql-case)
- [GROUP BY and aggregate functions](#/kb/sql-group-by)
- [NULL: IS NULL, COALESCE, COUNT(col) versus COUNT(*)](#/kb/sql-nulls)
- Official docs: https://www.sqlite.org/lang.html
