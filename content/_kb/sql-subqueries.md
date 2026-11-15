---
title: "Subqueries: scalar, IN, EXISTS, correlated"
summary: A query inside another query, used as one value, a list of values, an existence test or a table.
tags: [sql, subqueries]
---
```sql
-- scalar: one value
SELECT order_id, delivery_fee FROM orders
WHERE delivery_fee > (SELECT AVG(delivery_fee) FROM orders);

-- IN: a list of values
SELECT name FROM couriers
WHERE courier_id IN (SELECT courier_id FROM orders WHERE delivery_fee = 0);

-- EXISTS: is there at least one matching row?
SELECT name FROM restaurants AS r
WHERE EXISTS (SELECT 1 FROM orders AS o
              WHERE o.restaurant_id = r.restaurant_id AND o.coupon_code = 'PIZZA20');
```

- A subquery always goes in brackets.
- A scalar subquery must return one column and one row.
- `IN` needs a subquery with exactly one column.
- `EXISTS` ignores what is selected. `SELECT 1` is the usual habit.

<!-- more -->

## Details

A plain subquery runs once and does not look at the outer query. A correlated subquery uses a column of the outer row, so think of it as running once per outer row. The `EXISTS` example above is correlated through `r.restaurant_id`.

A correlated scalar subquery can compare each row with a value for its own group:

```sql
SELECT o.order_id, o.courier_id, o.actual_minutes
FROM orders AS o
WHERE o.actual_minutes > 1.8 * (
  SELECT AVG(o2.actual_minutes)
  FROM orders AS o2
  WHERE o2.courier_id = o.courier_id
);
```

A subquery in `FROM` (a derived table) acts as a table. Give it an alias:

```sql
SELECT ROUND(AVG(n), 1) AS avg_orders_per_customer
FROM (SELECT customer_id, COUNT(*) AS n
      FROM orders
      GROUP BY customer_id) AS per_customer;
```

A scalar subquery can also sit in the `SELECT` list. If it finds no row, its value is NULL.

`IN` versus `EXISTS`: both answer "is there a match". `NOT IN` breaks when the list contains a NULL: the test is never true and you get no rows. `NOT EXISTS` does not have this problem.

Dialects: all of this is standard. MySQL and Postgres before version 16 require the alias on a derived table; SQLite and BigQuery do not. If a scalar subquery returns several rows, SQLite silently uses the first one, while Postgres, MySQL and BigQuery raise an error.

## Common mistakes

- Using `=` with a subquery that can return several rows. Use `IN`, or make it return one row.
- Using `NOT IN` on a column that can be NULL (like `courier_id` in orders).
- Giving the inner table no alias in a correlated subquery, so `courier_id = courier_id` compares a column with itself.
- Selecting two columns inside an `IN` subquery.

## See also

- [Common table expressions (WITH)](#/kb/sql-cte)
- [LEFT JOIN and anti-joins (rows with no match)](#/kb/sql-left-join-anti-join)
- [NULL: IS NULL, COALESCE, COUNT(col) versus COUNT(*)](#/kb/sql-nulls)
- Official docs: https://www.sqlite.org/lang.html
