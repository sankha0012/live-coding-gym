---
title: NTILE, FIRST_VALUE and LAST_VALUE
summary: NTILE splits ordered rows into equal buckets; FIRST_VALUE and LAST_VALUE read the first or last row of the frame.
tags: [sql, window]
---
```sql
WITH per_courier AS (
  SELECT courier_id, COUNT(*) AS orders
  FROM orders
  WHERE courier_id IS NOT NULL
  GROUP BY courier_id
)
SELECT courier_id, orders,
       NTILE(4) OVER (ORDER BY orders DESC, courier_id)           AS quartile,
       FIRST_VALUE(orders) OVER (ORDER BY orders DESC, courier_id) AS top_orders
FROM per_courier;
```

- `NTILE(n)` numbers the buckets 1 to `n` in the window's order. Bucket 1 comes first.
- `FIRST_VALUE(col)` returns `col` from the first row of the frame.
- `LAST_VALUE` needs an explicit frame, or it returns the current row.

<!-- more -->

## Details

`NTILE(n)` sorts the partition and deals the rows into `n` groups of nearly equal size. If the rows do not divide evenly, the first buckets get one extra row: 10 rows with `NTILE(4)` give sizes 3, 3, 2, 2. It splits by row count, not by value, so two rows with the same value can land in different buckets. Add a tie-breaker to keep the result stable.

`FIRST_VALUE` and `LAST_VALUE` read from the window frame. With `ORDER BY` and no frame clause, the frame ends at the current row. So `FIRST_VALUE` works as expected, but `LAST_VALUE` just returns the current row. Extend the frame to the end of the partition:

```sql
SELECT courier_id, order_id, created_at,
       FIRST_VALUE(order_id) OVER w AS first_order,
       LAST_VALUE(order_id)  OVER w AS last_order
FROM orders
WHERE courier_id IN (1, 2)
WINDOW w AS (
  PARTITION BY courier_id
  ORDER BY created_at, order_id
  ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
)
ORDER BY courier_id, created_at, order_id;
```

A simpler way to get the last value is `FIRST_VALUE` with the order reversed (`ORDER BY created_at DESC`).

Unlike `MIN` and `MAX`, these return any column of the first or last row, not only the column you sort by. That is how you attach "the restaurant of the customer's first order" to every row.

`NTH_VALUE(col, n)` returns the value from row `n` of the frame, with the same frame rule.

Dialects: all three work in SQLite 3.25+, Postgres, MySQL 8+ and BigQuery. Postgres and BigQuery also have percentile functions; SQLite does not.

## Common mistakes

- Using `LAST_VALUE` with the default frame and getting the current row back.
- Expecting `NTILE` to put equal values in the same bucket. It only counts rows.
- Forgetting `DESC` when bucket 1 should hold the highest values.
- Running `NTILE(4)` on fewer than 4 rows and expecting 4 buckets. You get one bucket per row.

## See also

- [Window functions: OVER, PARTITION BY, ORDER BY](#/kb/sql-window-functions)
- [Running totals, moving averages and window frames](#/kb/sql-running-totals-frames)
- [ROW_NUMBER, RANK and DENSE_RANK](#/kb/sql-row-number-rank)
- Official docs: https://www.sqlite.org/windowfunctions.html
