---
title: "Data-quality queries: nulls, duplicates, orphans, ranges"
summary: Short queries to check a table before trusting it - row counts, NULLs, duplicate keys, orphans and odd values.
tags: [sql, data-quality]
---
```sql
SELECT COUNT(*)                          AS row_count,
       COUNT(DISTINCT order_id)          AS distinct_ids,   -- should equal row_count
       SUM(subtotal IS NULL)             AS null_subtotal,
       SUM(delivery_fee < 0)             AS negative_fee,
       SUM(status NOT IN ('delivered', 'cancelled')) AS bad_status,
       MIN(created_at)                   AS first_ts,
       MAX(created_at)                   AS last_ts
FROM orders;
```

- Nulls: `SUM(col IS NULL)`, or `COUNT(*) - COUNT(col)`.
- Duplicates: `GROUP BY key HAVING COUNT(*) > 1`.
- Orphans: `LEFT JOIN parent ... WHERE parent.key IS NULL`.
- Ranges: `MIN`, `MAX` and a count of values outside the allowed range.

<!-- more -->

## Details

Run these checks before writing the real query, and say out loud what you expect. Each check should return 0 or an empty result when the data is clean.

Duplicate keys. The key can be several columns:

```sql
SELECT order_id, COUNT(*) AS n
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;
```

Orphans: child rows whose foreign key points to no parent row. Rows with a NULL key are a different case, so exclude them:

```sql
SELECT o.order_id, o.courier_id
FROM orders AS o
LEFT JOIN couriers AS k ON k.courier_id = o.courier_id
WHERE o.courier_id IS NOT NULL
  AND k.courier_id IS NULL;
```

Rules between columns. Count the rows that break a business rule:

```sql
SELECT SUM(status = 'cancelled' AND actual_minutes IS NOT NULL) AS cancelled_with_time,
       SUM(status = 'delivered' AND courier_id IS NULL)         AS delivered_no_courier,
       SUM(actual_minutes <= 0 OR actual_minutes > 240)         AS odd_minutes
FROM orders;
```

Other useful checks:

- Allowed values: `SELECT status, COUNT(*) FROM orders GROUP BY status` shows typos and case differences.
- Join fan-out: compare `COUNT(*)` before and after a join. If it grows, the join key is not unique on the other side.
- Freshness and gaps: `MAX(created_at)`, and orders per day to spot missing days.
- Text hygiene: `col <> TRIM(col)` finds stray spaces; `col = ''` finds empty strings that are not NULL.

Dialects: `SUM(condition)` works in SQLite and MySQL because a comparison is 0 or 1. In Postgres write `COUNT(*) FILTER (WHERE condition)`, in BigQuery `COUNTIF(condition)`. `SUM(CASE WHEN condition THEN 1 ELSE 0 END)` works everywhere.

## Common mistakes

- Checking only for NULL and missing empty strings, zeros or placeholder values like `'N/A'`.
- Treating a NULL foreign key as an orphan. NULL means "none"; an orphan is a value with no parent.
- A `SUM(condition)` where the condition is NULL for some rows. Those rows count as 0, not as failures.
- Checking the key of one table but not the uniqueness of the key you are about to join on.

## See also

- [NULL: IS NULL, COALESCE, COUNT(col) versus COUNT(*)](#/kb/sql-nulls)
- [De-duplicating rows](#/kb/sql-dedupe)
- [LEFT JOIN and anti-joins (rows with no match)](#/kb/sql-left-join-anti-join)
- [HAVING](#/kb/sql-having)
