---
title: Self joins
summary: Join a table to itself with two aliases to compare rows of the same table.
tags: [sql, joins]
---
```sql
-- pairs of restaurants with the same city and cuisine
SELECT a.name AS first, b.name AS second, a.city, a.cuisine
FROM restaurants AS a
JOIN restaurants AS b
  ON b.city = a.city
 AND b.cuisine = a.cuisine
 AND b.restaurant_id > a.restaurant_id;
```

- The same table appears twice, so both copies need an alias.
- `b.id > a.id` drops a row paired with itself and keeps each pair once.
- Use `<>` instead of `>` when you want both (A, B) and (B, A).

<!-- more -->

## Details

A self join is a normal join. The only special part is that the left and the right table are the same, so the aliases are what tell the two copies apart. Think of `a` as "this row" and `b` as "the other row".

Typical uses: find pairs that share a value, compare a row with an earlier or later row, or follow a parent key that points to the same table.

Example: orders placed by the same customer less than one hour after an earlier order.

```sql
SELECT a.customer_id,
       a.order_id AS first_order,
       b.order_id AS next_order
FROM orders AS a
JOIN orders AS b
  ON b.customer_id = a.customer_id
 AND b.created_at > a.created_at
 AND julianday(b.created_at) - julianday(a.created_at) < 1.0 / 24
ORDER BY a.customer_id, a.order_id;
```

A self join can produce many rows: a group of `n` matching rows gives `n * (n - 1) / 2` pairs. If you only need one row per key, add `SELECT DISTINCT` or group the result.

For "previous row" and "next row" comparisons, a window function (`LAG`, `LEAD`) is usually shorter and faster than a self join.

Dialects: the syntax is the same in SQLite, Postgres, MySQL and BigQuery.

## Common mistakes

- Forgetting the inequality on the key, so every row matches itself.
- Using `<>` when each pair should appear once. You get every pair twice.
- Leaving a column without an alias prefix. Every column name is ambiguous in a self join.
- Joining only on a low-detail column (like `city`) and getting a huge result. Add every condition that defines a pair.

## See also

- [INNER JOIN](#/kb/sql-joins)
- [LAG and LEAD](#/kb/sql-lag-lead)
- [De-duplicating rows](#/kb/sql-dedupe)
- Official docs: https://www.sqlite.org/lang.html
