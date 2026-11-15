---
title: "Window functions: OVER, PARTITION BY, ORDER BY"
summary: Compute a value across related rows with OVER (...) while keeping every row.
tags: [sql, window]
---
```sql
SELECT order_id, courier_id, delivery_fee,
       COUNT(*)          OVER (PARTITION BY courier_id) AS courier_orders,
       SUM(delivery_fee) OVER (PARTITION BY courier_id) AS courier_fees,
       SUM(delivery_fee) OVER ()                        AS all_fees,
       ROW_NUMBER() OVER (PARTITION BY courier_id ORDER BY created_at) AS nth
FROM orders
WHERE courier_id IS NOT NULL;
```

- `OVER (...)` turns a function into a window function. Rows are not collapsed.
- `PARTITION BY` splits rows into groups. Empty `OVER ()` means all rows.
- `ORDER BY` inside `OVER` sets the order within each partition.

<!-- more -->

## Details

`GROUP BY` returns one row per group. A window function returns one value per input row, computed from the rows of that row's partition. So you can show a detail row next to a group total.

Kinds of window functions:

- Aggregates: `SUM`, `AVG`, `COUNT`, `MIN`, `MAX` with `OVER`.
- Ranking: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `NTILE`.
- Offset: `LAG`, `LEAD`, `FIRST_VALUE`, `LAST_VALUE`.

Window functions run after `WHERE`, `GROUP BY` and `HAVING`, and before the final `ORDER BY`. This means they are not allowed in `WHERE`. Compute them in a CTE or subquery, then filter:

```sql
WITH per_courier AS (
  SELECT k.vehicle, k.name, COUNT(*) AS orders
  FROM orders AS o
  JOIN couriers AS k ON k.courier_id = o.courier_id
  GROUP BY k.vehicle, k.name
)
SELECT vehicle, name, orders,
       ROUND(100.0 * orders / SUM(orders) OVER (PARTITION BY vehicle), 1) AS pct_of_vehicle
FROM per_courier
ORDER BY vehicle, orders DESC;
```

Adding `ORDER BY` inside `OVER` changes aggregates: `SUM(x) OVER (ORDER BY d)` becomes a running total, not a grand total.

If several functions share a window, name it once with a `WINDOW` clause after `HAVING`: `SUM(x) OVER w ... WINDOW w AS (PARTITION BY courier_id ORDER BY created_at)`.

Dialects: window functions need SQLite 3.25+, MySQL 8+, and work in Postgres and BigQuery. BigQuery also has `QUALIFY` to filter on a window function without a subquery.

## Common mistakes

- Using a window function in `WHERE` or `HAVING`. Wrap the query and filter outside.
- Forgetting `PARTITION BY`, so the value is computed over the whole table.
- Thinking the `ORDER BY` inside `OVER` sorts the output. Add a final `ORDER BY` too.
- Adding `ORDER BY` to `SUM(...) OVER` when a group total was wanted.

## See also

- [ROW_NUMBER, RANK and DENSE_RANK](#/kb/sql-row-number-rank)
- [LAG and LEAD](#/kb/sql-lag-lead)
- [Running totals, moving averages and window frames](#/kb/sql-running-totals-frames)
- Official docs: https://www.sqlite.org/windowfunctions.html
