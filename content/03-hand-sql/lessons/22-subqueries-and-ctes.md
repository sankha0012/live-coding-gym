# Subqueries and CTEs

## The problem it solves

Some questions need two steps. "Customers who spend more than the average customer." First compute the average, then compare. A subquery or a CTE (common table expression) lets you do step one inside the same statement and name the result.

## The smallest example

Tables used: `orders`, `customers`.

A scalar subquery returns exactly one value:

```sql
SELECT order_id, subtotal
FROM orders
WHERE subtotal > (SELECT AVG(subtotal) FROM orders)
ORDER BY subtotal DESC, order_id
LIMIT 3;
```

An `IN` subquery returns a list:

```sql
SELECT customer_id, name
FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders WHERE status = 'cancelled')
ORDER BY customer_id
LIMIT 5;
```

A correlated subquery uses a column from the outer row, so it runs once for each outer row. Orders above the average of their own restaurant:

```sql
SELECT o.order_id, o.restaurant_id, o.subtotal
FROM orders o
WHERE o.subtotal > (SELECT AVG(i.subtotal) FROM orders i
                    WHERE i.restaurant_id = o.restaurant_id)
ORDER BY o.order_id
LIMIT 5;
```

It is easy to read and fine at this size. On large tables a join to a pre-grouped result is usually faster.

## CTEs: name your steps

A CTE starts with `WITH`. It is a named query you can use below it, like a temporary view. It makes long queries readable, and in an interview it shows you think in steps.

```sql
WITH per_customer AS (
    SELECT customer_id, SUM(subtotal) AS spend
    FROM orders
    WHERE status = 'delivered'
    GROUP BY customer_id
)
SELECT customer_id, ROUND(spend, 2) AS spend
FROM per_customer
WHERE spend > (SELECT AVG(spend) FROM per_customer)
ORDER BY spend DESC, customer_id
LIMIT 5;
```

Chain several CTEs with commas. Each one can read the ones above it:

```sql
WITH delivered AS (
    SELECT * FROM orders WHERE status = 'delivered'
),
by_city AS (
    SELECT r.city, COUNT(*) AS n
    FROM delivered d
    JOIN restaurants r ON r.restaurant_id = d.restaurant_id
    GROUP BY r.city
)
SELECT city, n FROM by_city ORDER BY n DESC, city;
```

Write each step so it does one thing, and check each step alone by running `SELECT * FROM step`.

## Subquery in FROM

You can also put a subquery in the `FROM` clause. It needs an alias. This is the same idea as a CTE, only written inline. A CTE reads better when you use the result twice.

```sql
SELECT AVG(n) AS avg_orders_per_customer
FROM (SELECT customer_id, COUNT(*) AS n FROM orders GROUP BY customer_id) t;
```

## The three traps

1. **NOT IN and NULL.** `x NOT IN (SELECT y ...)` returns no rows at all if the list contains a single NULL, because `x <> NULL` is unknown. Use `NOT EXISTS`, or a LEFT JOIN with `IS NULL`, or add `WHERE y IS NOT NULL` inside.
2. **A scalar subquery that returns many rows.** `= (SELECT ...)` expects one value. SQLite quietly takes the first row; Postgres raises an error. Make sure the subquery aggregates, or uses `LIMIT 1` with a clear `ORDER BY`.
3. **Thinking a CTE is cached.** In most engines a CTE is just a name for a query. If you use it three times it may run three times. For an interview this is fine; in production, check the plan.

## Say it like this

"I split the problem in two. First a CTE that computes spend per customer, then an outer query that compares each customer with the average of that CTE. I prefer a CTE over a nested subquery because the steps have names and I can test each one alone. For the opposite question, customers with no order, I use NOT EXISTS instead of NOT IN, because NOT IN returns nothing when the list contains a NULL."
