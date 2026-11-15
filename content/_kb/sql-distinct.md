---
title: DISTINCT and COUNT(DISTINCT)
summary: Remove repeated rows with SELECT DISTINCT and count different values with COUNT(DISTINCT col).
tags: [sql, aggregation]
---
```sql
SELECT DISTINCT city, cuisine      -- one row per (city, cuisine) pair
FROM restaurants;

SELECT COUNT(*)                    AS order_rows,
       COUNT(DISTINCT courier_id)  AS couriers_used
FROM orders;
```

- `DISTINCT` applies to the whole row of selected columns, not to the first column only.
- `COUNT(DISTINCT col)` counts different non-NULL values.
- `COUNT(*)` counts rows, repeated values included.

<!-- more -->

## Details

`SELECT DISTINCT` runs after the columns are computed. Two rows are duplicates when every selected column is equal. NULL counts as equal to NULL here, so one NULL row is kept.

`COUNT(DISTINCT col)` works per group, like any aggregate:

```sql
SELECT r.city,
       COUNT(*)                      AS orders,
       COUNT(DISTINCT o.customer_id) AS customers
FROM orders AS o
JOIN restaurants AS r ON r.restaurant_id = o.restaurant_id
GROUP BY r.city
ORDER BY r.city;
```

This is the usual fix after a join that repeats rows: count the key with `DISTINCT` instead of counting rows.

`SUM(DISTINCT col)` and `AVG(DISTINCT col)` also exist but are rarely what you want.

To count different pairs in SQLite, count the rows of a `DISTINCT` subquery:

```sql
SELECT COUNT(*) AS pairs
FROM (SELECT DISTINCT customer_id, restaurant_id FROM orders);
```

Dialects: SQLite allows only one column inside `COUNT(DISTINCT ...)`. Postgres accepts `COUNT(DISTINCT (a, b))` and MySQL accepts `COUNT(DISTINCT a, b)`. BigQuery also has `APPROX_COUNT_DISTINCT(col)` for large tables.

## Common mistakes

- Writing `SELECT DISTINCT(city), name` and expecting one row per city. The brackets do nothing; the row is still (city, name).
- Using `DISTINCT` to hide duplicates made by a wrong join. Fix the join condition first.
- Forgetting that `COUNT(DISTINCT col)` skips NULL. A column with only NULLs gives 0.
- Writing `DISTINCT COUNT(col)`. The keyword goes inside the brackets: `COUNT(DISTINCT col)`.

## See also

- [GROUP BY and aggregate functions](#/kb/sql-group-by)
- [De-duplicating rows](#/kb/sql-dedupe)
- [NULL: IS NULL, COALESCE, COUNT(col) versus COUNT(*)](#/kb/sql-nulls)
- Official docs: https://www.sqlite.org/lang.html
