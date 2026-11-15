---
title: "Dialect differences: SQLite, Postgres, BigQuery, MySQL"
summary: The same query in four dialects - what changes for dates, strings, booleans, division and row filters.
tags: [sql, dialects]
---
```sql
-- SQLite (what this app runs)
SELECT strftime('%Y-%m', created_at)             AS month,
       'M' || strftime('%m', created_at)         AS label,
       COUNT(*)                                  AS orders,
       SUM(status = 'cancelled')                 AS cancelled,
       ROUND(1.0 * SUM(status = 'cancelled') / COUNT(*), 3) AS cancel_rate
FROM orders
GROUP BY month, label
LIMIT 5;
```

- Month: Postgres `DATE_TRUNC('month', ts)`, BigQuery `DATE_TRUNC(d, MONTH)`, MySQL `DATE_FORMAT(ts, '%Y-%m')`.
- Count a condition: Postgres `COUNT(*) FILTER (WHERE ...)`, BigQuery `COUNTIF(...)`. `SUM(CASE ...)` works everywhere.
- Join text: `||` in SQLite and Postgres, `CONCAT(a, b)` in MySQL and BigQuery.

<!-- more -->

## Details

The core of SQL is the same everywhere: `SELECT`, joins, `GROUP BY`, `HAVING`, `CASE`, CTEs and window functions. The differences are in functions and in how strict the engine is.

Dates:

- Day difference: SQLite `julianday(b) - julianday(a)`; Postgres `b::date - a::date`; BigQuery `DATE_DIFF(b, a, DAY)`; MySQL `DATEDIFF(b, a)`.
- Add time: SQLite `date(x, '+7 days')`; Postgres `x + INTERVAL '7 days'`; BigQuery `DATE_ADD(x, INTERVAL 7 DAY)`; MySQL `x + INTERVAL 7 DAY`.
- Today: SQLite `date('now')`; Postgres and MySQL `CURRENT_DATE`; BigQuery `CURRENT_DATE()`.

Numbers and types:

- Integer division: `7 / 2` is 3 in SQLite and Postgres, 3.5 in MySQL and BigQuery. Multiply by `1.0` to be safe.
- Cast: `CAST(x AS INTEGER)` works everywhere. Postgres also has `x::int`. BigQuery names are `INT64`, `FLOAT64`, `STRING`.

Strictness:

- Selecting a column that is not grouped: allowed in SQLite, an error in Postgres and BigQuery, an error in MySQL by default.
- Alias in `HAVING`: fine in SQLite, MySQL and BigQuery, an error in Postgres.
- Quotes: single quotes for text everywhere. Identifiers use double quotes in SQLite and Postgres, backticks in MySQL and BigQuery.
- `LIKE` is case-insensitive in SQLite and MySQL, case-sensitive in Postgres (which adds `ILIKE`) and BigQuery.
- NULL order with `ASC`: first in SQLite, MySQL and BigQuery, last in Postgres.

Extras: Postgres has `DISTINCT ON`. BigQuery has `QUALIFY` to filter on a window function, and `SAFE_DIVIDE(a, b)`.

This portable version of the brief query runs in every dialect except for the month expression:

```sql
SELECT strftime('%Y-%m', created_at) AS month,
       COUNT(*) AS orders,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled
FROM orders
GROUP BY strftime('%Y-%m', created_at)
ORDER BY 1;
```

## Common mistakes

- Using `SUM(a = b)` in Postgres or BigQuery. A boolean cannot be summed there.
- Forgetting `1.0 *` and getting 0 for every rate in SQLite or Postgres.
- Using double quotes for text out of habit. MySQL accepts it; Postgres reads it as a column name.
- Assuming a function exists everywhere: `strftime`, `julianday`, `IFNULL` and `GROUP_CONCAT` are not in Postgres.

## See also

- [Dates in SQLite: strftime, date, julianday](#/kb/sql-dates-sqlite)
- [Conditional aggregation (CASE inside SUM, AVG, COUNT)](#/kb/sql-conditional-aggregation)
- [NULL: IS NULL, COALESCE, COUNT(col) versus COUNT(*)](#/kb/sql-nulls)
- Official docs: https://www.sqlite.org/lang.html
