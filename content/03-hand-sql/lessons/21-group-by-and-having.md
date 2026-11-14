# GROUP BY and HAVING

## The problem it solves

You rarely want rows. You want numbers per something: orders per city, average delay per cuisine, revenue per month. `GROUP BY` collapses many rows into one row per group, and aggregate functions compute one number for each group.

## The smallest example

Tables used: `orders`.

```sql
SELECT status, COUNT(*) AS n, ROUND(AVG(actual_minutes), 1) AS avg_minutes
FROM orders
GROUP BY status
ORDER BY status;
```

Rule: every column in the SELECT list is either in the `GROUP BY` or inside an aggregate such as `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. SQLite is lenient and lets you break this rule, and then it returns an arbitrary row's value. Postgres and BigQuery raise an error. Always follow the strict rule.

## The order the database thinks in

Read a query in this order, not top to bottom:

1. `FROM` and `JOIN`: build the rows.
2. `WHERE`: remove rows.
3. `GROUP BY`: make groups.
4. `HAVING`: remove groups.
5. `SELECT`: compute the output columns and aliases.
6. `ORDER BY`, then `LIMIT`.

This explains most beginner errors. `WHERE` runs before the groups exist, so it cannot use `COUNT(*)`. `HAVING` runs after, so it can.

```sql
SELECT r.cuisine, COUNT(*) AS delivered
FROM orders o
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered'
GROUP BY r.cuisine
HAVING COUNT(*) >= 200
ORDER BY delivered DESC, r.cuisine;
```

`WHERE` filters rows, `HAVING` filters groups. If a condition does not need an aggregate, prefer `WHERE`, because it removes rows earlier and the query is faster.

## Several group columns and conditional aggregates

Group by two columns to get one row per pair:

```sql
SELECT r.city, o.status, COUNT(*) AS n
FROM orders o
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY r.city, o.status
ORDER BY r.city, o.status;
```

To get a rate, put a `CASE` inside the aggregate. This is the most useful trick in interviews:

```sql
SELECT r.city,
       COUNT(*) AS orders,
       SUM(CASE WHEN o.status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled,
       ROUND(AVG(CASE WHEN o.status = 'cancelled' THEN 1.0 ELSE 0 END), 3) AS cancel_rate
FROM orders o
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY r.city
ORDER BY cancel_rate DESC, r.city;
```

The average of a 1 or 0 column is the share of ones. Use `1.0`, not `1`, so the value is a decimal in every database.

## The three traps

1. **WHERE versus HAVING.** `WHERE COUNT(*) > 5` is an error. Use `HAVING COUNT(*) > 5`. And `HAVING status = 'delivered'` runs in SQLite but is an error in Postgres; it belongs in `WHERE`.
2. **NULLs in aggregates.** `AVG`, `SUM`, `MIN` and `MAX` skip NULLs, and `COUNT(col)` skips them too. Cancelled orders have no `actual_minutes`, so `AVG(actual_minutes)` leaves them out. If NULL should count as zero, write `COALESCE` inside the aggregate. A group where every value is NULL returns NULL for `SUM`, not 0.
3. **Grouping by the wrong grain.** If you group by `customer_id` and `city` but a customer has one city, fine. If the second column can vary inside a customer, you get several rows per customer and your "per customer" answer is wrong. Say the grain out loud: "one row per city and status".

## Say it like this

"I filter the rows I care about in WHERE, group by the columns the question asks for, and aggregate. If the question filters on a group value, like at least 200 orders, I use HAVING because it runs after grouping. For a rate I average a CASE that gives 1 or 0. I also watch NULLs, because AVG and COUNT of a column skip them, and I state the grain of my output, one row per city and status."
