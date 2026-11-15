---
title: ROW_NUMBER, RANK and DENSE_RANK
summary: Number rows inside each partition; the three functions differ only in how they treat ties.
tags: [sql, window]
---
```sql
SELECT vehicle, courier_id, orders,
       ROW_NUMBER() OVER w AS rn,     -- 1, 2, 3, 4   ties get different numbers
       RANK()       OVER w AS rnk,    -- 1, 2, 2, 4   ties share, then a gap
       DENSE_RANK() OVER w AS drnk    -- 1, 2, 2, 3   ties share, no gap
FROM (SELECT k.vehicle, o.courier_id, COUNT(*) AS orders
      FROM orders AS o JOIN couriers AS k ON k.courier_id = o.courier_id
      GROUP BY k.vehicle, o.courier_id)
WINDOW w AS (PARTITION BY vehicle ORDER BY orders DESC);
```

- The `ORDER BY` inside `OVER` decides who gets number 1.
- `PARTITION BY` restarts the numbering for each group.
- These functions take no argument: `ROW_NUMBER()`.

<!-- more -->

## Details

Pick the function by what a tie should do:

- `ROW_NUMBER`: exactly one row per number. Use it for "one row per group" and "top N rows".
- `RANK`: equal values share a rank, and the next rank skips (like sports).
- `DENSE_RANK`: equal values share a rank with no skip. Use it for "the Nth highest value".

With `ROW_NUMBER`, tied rows get numbers in an arbitrary order. Add a tie-breaker to the window's `ORDER BY` to make the result stable.

A window function cannot be used in `WHERE`, so top-N-per-group needs two steps: number the rows in a CTE, then filter on the number.

```sql
WITH ranked AS (
  SELECT courier_id, order_id, actual_minutes,
         ROW_NUMBER() OVER (
           PARTITION BY courier_id
           ORDER BY actual_minutes, order_id
         ) AS rn
  FROM orders
  WHERE status = 'delivered'
)
SELECT courier_id, order_id, actual_minutes
FROM ranked
WHERE rn <= 2
ORDER BY courier_id, rn;
```

This returns the two fastest deliveries of each courier. Change `rn <= 2` to `rn = 1` for one row per courier.

Dialects: the three functions are the same in SQLite 3.25+, Postgres, MySQL 8+ and BigQuery. BigQuery can filter directly with `QUALIFY rn <= 2`. Postgres has `DISTINCT ON` as a shortcut for "first row per group".

## Common mistakes

- Filtering with `WHERE ROW_NUMBER() OVER (...) = 1` in the same query. This is an error.
- Leaving `ORDER BY` out of the window. The numbering is then arbitrary.
- Using `RANK` for "top 3 rows per group". With ties you can get more than 3 rows, or no row with rank 2.
- Forgetting `DESC` when the highest value should be number 1.
- Using `ROW_NUMBER` with no tie-breaker and getting different rows on each run.

## See also

- [Window functions: OVER, PARTITION BY, ORDER BY](#/kb/sql-window-functions)
- [De-duplicating rows](#/kb/sql-dedupe)
- [NTILE, FIRST_VALUE and LAST_VALUE](#/kb/sql-ntile-first-value)
- Official docs: https://www.sqlite.org/windowfunctions.html
