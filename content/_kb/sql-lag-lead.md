---
title: LAG and LEAD
summary: Read a value from the previous row (LAG) or the next row (LEAD) of the same partition.
tags: [sql, window]
---
```sql
WITH daily AS (
  SELECT date(created_at) AS day, COUNT(*) AS orders
  FROM orders
  GROUP BY day
)
SELECT day, orders,
       LAG(orders)  OVER (ORDER BY day) AS prev_orders,
       orders - LAG(orders) OVER (ORDER BY day) AS diff,
       LEAD(orders) OVER (ORDER BY day) AS next_orders
FROM daily;
```

- `LAG(col)` is the value one row back. `LEAD(col)` is one row ahead.
- The `ORDER BY` inside `OVER` defines what "previous" and "next" mean. It is required.
- The first row has no previous row, so `LAG` returns NULL there.

<!-- more -->

## Details

Full form: `LAG(expr, offset, default) OVER (PARTITION BY ... ORDER BY ...)`. `offset` is how many rows back (default 1). `default` is the value returned when there is no such row (default NULL).

With `PARTITION BY`, the function never looks outside the row's own partition. Each partition's first row gets NULL from `LAG`, and its last row gets NULL from `LEAD`:

```sql
SELECT courier_id, order_id, created_at,
       LAG(created_at) OVER (
         PARTITION BY courier_id ORDER BY created_at, order_id
       ) AS prev_created_at,
       LAG(order_id, 2, -1) OVER (
         PARTITION BY courier_id ORDER BY created_at, order_id
       ) AS two_back
FROM orders
WHERE courier_id IN (1, 2)
ORDER BY courier_id, created_at, order_id;
```

Typical uses: change from the previous period (`x - LAG(x)`), growth rate (`1.0 * x / LAG(x) - 1`), and time between events (`julianday(created_at) - julianday(LAG(created_at) ...)`).

`LAG` reads the previous row, not the previous calendar period. If a day or month has no rows, it is simply missing, and "previous" jumps over the gap.

You usually aggregate first (one row per day or month in a CTE) and apply `LAG` on that result. A window function cannot be used in `WHERE`; to filter on the difference, wrap the query in another CTE.

Dialects: `LAG` and `LEAD` are the same in SQLite 3.25+, Postgres, MySQL 8+ and BigQuery.

## Common mistakes

- Leaving `ORDER BY` out of `OVER`. The previous row is then arbitrary.
- Forgetting `PARTITION BY`, so the first row of one group reads the last row of another.
- Doing math with the NULL of the first row and not expecting a NULL result. Use the third argument or `COALESCE` if you need 0.
- Dividing integers for a growth rate: `orders / LAG(orders)` is integer division in SQLite. Multiply by `1.0`.
- Mixing up the direction: with `ORDER BY day DESC`, `LAG` returns the later day.

## See also

- [Window functions: OVER, PARTITION BY, ORDER BY](#/kb/sql-window-functions)
- [Running totals, moving averages and window frames](#/kb/sql-running-totals-frames)
- [Dates in SQLite: strftime, date, julianday](#/kb/sql-dates-sqlite)
- Official docs: https://www.sqlite.org/windowfunctions.html
