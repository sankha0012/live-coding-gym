---
title: De-duplicating rows
summary: Find duplicates with GROUP BY and HAVING, and keep one row per key with ROW_NUMBER.
tags: [sql, data-quality]
---
```sql
WITH numbered AS (
  SELECT *,
         ROW_NUMBER() OVER (
           PARTITION BY customer_id, date(created_at)   -- what "duplicate" means
           ORDER BY created_at, order_id                -- which row to keep
         ) AS rn
  FROM orders
)
SELECT order_id, customer_id, created_at
FROM numbered
WHERE rn = 1;
```

- `PARTITION BY` lists the columns that define a duplicate.
- The window's `ORDER BY` decides which row survives. Row 1 is kept.
- Add a unique tie-breaker (like the id) so the choice is stable.

<!-- more -->

## Details

First decide the key: which columns must be equal for two rows to count as the same thing. Then pick the tool.

To find duplicates, group by the key and keep groups with more than one row:

```sql
SELECT customer_id, date(created_at) AS day, COUNT(*) AS n
FROM orders
GROUP BY customer_id, day
HAVING COUNT(*) > 1
ORDER BY n DESC, customer_id;
```

To remove rows that are identical in every selected column, `SELECT DISTINCT` is enough. `GROUP BY` on all the columns does the same.

To keep one full row per key, use `ROW_NUMBER` as in the example above. This is the general pattern because you control which row wins: `ORDER BY created_at DESC` keeps the latest, `ASC` keeps the first.

To keep one row per key but only need an aggregate of the others, plain `GROUP BY` is simpler: `SELECT customer_id, MAX(created_at) FROM orders GROUP BY customer_id`.

To delete duplicates from a table in SQLite, keep the smallest `rowid` of each key: `DELETE FROM t WHERE rowid NOT IN (SELECT MIN(rowid) FROM t GROUP BY key_col)`.

Before a join, de-duplicate the "one" side. A duplicate key there repeats every matching row on the other side and inflates sums.

Dialects: the `ROW_NUMBER` pattern works everywhere. Postgres has a shortcut, `SELECT DISTINCT ON (key) ... ORDER BY key, created_at DESC`. BigQuery can skip the CTE with `QUALIFY ROW_NUMBER() OVER (...) = 1`.

## Common mistakes

- Using `SELECT DISTINCT` when rows differ in another column (a timestamp, an id). Nothing is removed.
- Using `RANK` in place of `ROW_NUMBER`. Tied rows all get 1 and the duplicates stay.
- No tie-breaker in the window's `ORDER BY`, so a different row is kept on each run.
- Selecting `MAX(created_at)` and other plain columns in one `GROUP BY` and assuming they come from the same row. Only SQLite does that, and only for a single `MIN` or `MAX`.
- Choosing a key that is too narrow and deleting rows that were real.

## See also

- [ROW_NUMBER, RANK and DENSE_RANK](#/kb/sql-row-number-rank)
- [DISTINCT and COUNT(DISTINCT)](#/kb/sql-distinct)
- [Data-quality queries: nulls, duplicates, orphans, ranges](#/kb/sql-data-quality-checks)
- Official docs: https://www.sqlite.org/lang.html
