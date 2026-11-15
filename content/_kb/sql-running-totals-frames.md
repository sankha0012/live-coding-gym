---
title: Running totals, moving averages and window frames
summary: Add ORDER BY and a ROWS frame to a window aggregate to get cumulative sums and moving averages.
tags: [sql, window]
---
```sql
WITH daily AS (
  SELECT date(created_at) AS day, SUM(delivery_fee) AS fees
  FROM orders
  GROUP BY day
)
SELECT day, fees,
       SUM(fees) OVER (ORDER BY day) AS running_fees,
       AVG(fees) OVER (ORDER BY day
                       ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avg_3d
FROM daily;
```

- `SUM(x) OVER (ORDER BY d)` is a running total: all rows up to the current one.
- `ROWS BETWEEN n PRECEDING AND CURRENT ROW` is a moving window of `n + 1` rows.
- Add `PARTITION BY` to restart the total for each group.

<!-- more -->

## Details

The frame is the set of rows, inside the partition, that the aggregate reads for the current row. It is written after the window's `ORDER BY`:

`ROWS BETWEEN <start> AND <end>`

Start and end can be `UNBOUNDED PRECEDING`, `n PRECEDING`, `CURRENT ROW`, `n FOLLOWING`, `UNBOUNDED FOLLOWING`.

Defaults:

- No `ORDER BY` in `OVER`: the frame is the whole partition.
- With `ORDER BY` and no frame: `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`.

`RANGE` treats rows with the same `ORDER BY` value as one block ("peers"), so tied rows all get the same running total. `ROWS` counts physical rows. When the order column can repeat, write `ROWS` explicitly or add a tie-breaker:

```sql
SELECT courier_id, order_id, delivery_fee,
       SUM(delivery_fee) OVER (
         PARTITION BY courier_id
         ORDER BY created_at, order_id
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS courier_running_fees
FROM orders
WHERE courier_id IN (1, 2)
ORDER BY courier_id, created_at, order_id;
```

At the start of a partition a moving frame has fewer rows: the second row of a 3-row average only averages 2 values. A `ROWS` frame counts rows, not days. If a day is missing from the data, "2 preceding" reaches further back in time.

A centred average uses `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING`. A share of the total uses an empty frame: `x / SUM(x) OVER ()`.

Dialects: frames work the same in SQLite 3.25+, Postgres, MySQL 8+ and BigQuery. `RANGE` with a numeric offset needs SQLite 3.28+.

## Common mistakes

- Writing `ROWS BETWEEN 3 PRECEDING AND CURRENT ROW` for a 3-row average. That is 4 rows.
- Relying on the default `RANGE` frame with duplicate order values, and getting the same total on tied rows.
- Putting the frame before `ORDER BY`. The order is `PARTITION BY`, `ORDER BY`, frame.
- Running the window on raw rows when the question is per day. Aggregate to one row per day first.

## See also

- [Window functions: OVER, PARTITION BY, ORDER BY](#/kb/sql-window-functions)
- [LAG and LEAD](#/kb/sql-lag-lead)
- [NTILE, FIRST_VALUE and LAST_VALUE](#/kb/sql-ntile-first-value)
- Official docs: https://www.sqlite.org/windowfunctions.html
