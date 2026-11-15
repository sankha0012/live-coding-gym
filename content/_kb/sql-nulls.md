---
title: "NULL: IS NULL, COALESCE, COUNT(col) versus COUNT(*)"
summary: NULL means unknown; test it with IS NULL, replace it with COALESCE, and remember aggregates skip it.
tags: [sql, nulls]
---
```sql
SELECT COUNT(*)                        AS all_rows,       -- every row
       COUNT(courier_id)               AS with_courier,   -- non-NULL only
       SUM(courier_id IS NULL)         AS without_courier,
       AVG(actual_minutes)             AS avg_known,      -- NULLs skipped
       AVG(COALESCE(actual_minutes, 0)) AS avg_null_as_0
FROM orders;

SELECT order_id, COALESCE(coupon_code, 'none') AS coupon
FROM orders
WHERE courier_id IS NULL;
```

- `col = NULL` is never true. Use `IS NULL` and `IS NOT NULL`.
- `COALESCE(a, b, ...)` returns the first argument that is not NULL.
- `COUNT(*)` counts rows. `COUNT(col)` counts rows where `col` is not NULL.
- `SUM`, `AVG`, `MIN`, `MAX` ignore NULL values.

<!-- more -->

## Details

NULL is "no value". Any arithmetic or comparison with NULL gives NULL: `NULL + 1`, `NULL = NULL`, `NULL <> 5`. `WHERE` keeps a row only when the condition is true, so a NULL result drops the row. This means `WHERE coupon_code <> 'PIZZA20'` also removes the rows with no coupon. To keep them:

```sql
SELECT COUNT(*) AS not_pizza20
FROM orders
WHERE coupon_code <> 'PIZZA20' OR coupon_code IS NULL;
```

Logic with NULL: `NULL AND false` is false, `NULL OR true` is true, everything else with NULL stays NULL.

Aggregates: if every value is NULL (or there are no rows), `SUM`, `AVG`, `MIN` and `MAX` return NULL and `COUNT` returns 0. Wrap the result when you need a number: `COALESCE(SUM(x), 0)`.

`NULLIF(a, b)` returns NULL when `a = b`. Its main use is avoiding division by zero: `x / NULLIF(y, 0)`.

For grouping, sorting and `DISTINCT`, NULLs are treated as equal to each other: `GROUP BY coupon_code` makes one group for all NULLs.

Dialects: `COALESCE` and `NULLIF` are standard. `IFNULL(a, b)` is the two-argument form in SQLite, MySQL and BigQuery. `SUM(col IS NULL)` works in SQLite and MySQL; elsewhere use `SUM(CASE WHEN col IS NULL THEN 1 ELSE 0 END)`. In SQLite an empty string `''` is not NULL.

## Common mistakes

- Writing `WHERE col = NULL` or `col != NULL`. Both return no rows.
- Using `NOT IN (subquery)` when the subquery can return NULL. The result is empty.
- Using `COUNT(col)` when you meant to count rows, or `COUNT(*)` after a LEFT JOIN when you meant matches.
- Replacing NULL with 0 before `AVG` without meaning to. It lowers the average.
- Adding columns where one can be NULL: `subtotal + delivery_fee` is NULL if either is NULL.

## See also

- [SELECT, WHERE and operators](#/kb/sql-select-where)
- [LEFT JOIN and anti-joins (rows with no match)](#/kb/sql-left-join-anti-join)
- [Data-quality queries: nulls, duplicates, orphans, ranges](#/kb/sql-data-quality-checks)
- Official docs: https://www.sqlite.org/lang.html
