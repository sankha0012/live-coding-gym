# Joins explained

## The problem it solves

Your data lives in several tables. An order has a `restaurant_id`, but the city is in `restaurants`. A join glues rows from two tables together when a condition is true. Almost every interview query starts with a join, so you must be able to type one without thinking.

## The smallest example

Tables used: `orders`, `restaurants`.

```sql
SELECT o.order_id, r.name, r.city
FROM orders o
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.order_id <= 100003
ORDER BY o.order_id;
```

`JOIN` alone means `INNER JOIN`. A row stays only if the `ON` condition finds a partner. The letters `o` and `r` are aliases. Use them, because they make every column name short and unambiguous.

Think of the shape in your head: the left table, the word JOIN, the right table, ON, and the key on both sides. Type that skeleton first, then fill in the SELECT list.

## The four kinds you need

- `INNER JOIN`: only rows with a match on both sides.
- `LEFT JOIN`: every row from the left table. If the right side has no match, its columns are NULL.
- `RIGHT JOIN` and `FULL JOIN`: rare. SQLite supports them since 3.39, but you can always swap the table order and use LEFT.
- `CROSS JOIN`: every left row with every right row. Rarely wanted.

## Finding rows with no match

The classic use of a LEFT JOIN is the anti-join: customers who never ordered.

```sql
SELECT c.customer_id, c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id
LIMIT 5;
```

The join keeps every customer. Customers with no order get NULL in the order columns. The `WHERE ... IS NULL` keeps only those. Test the key column of the right table, a column that can never be NULL when a match exists.

The same idea with `NOT EXISTS` reads more like English and is safe with NULLs:

```sql
SELECT c.customer_id
FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
LIMIT 5;
```

## Joining three tables and a table to itself

Chain joins one after another. Each `ON` links the new table to one already in the query.

```sql
SELECT c.city AS customer_city, r.city AS restaurant_city, COUNT(*) AS n
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN restaurants r ON r.restaurant_id = o.restaurant_id
GROUP BY c.city, r.city
ORDER BY n DESC, customer_city, restaurant_city
LIMIT 5;
```

A self join uses the same table twice under two aliases. To find pairs of orders by the same customer at the same restaurant:

```sql
SELECT a.customer_id, a.order_id AS first_order, b.order_id AS second_order
FROM orders a
JOIN orders b
  ON b.customer_id = a.customer_id
 AND b.restaurant_id = a.restaurant_id
 AND b.order_id > a.order_id
ORDER BY a.customer_id, first_order, second_order
LIMIT 5;
```

The condition `b.order_id > a.order_id` keeps each pair once and drops a row paired with itself.

## The three traps

1. **The filter that kills the LEFT JOIN.** If you write `LEFT JOIN orders o ON ... WHERE o.status = 'delivered'`, rows with NULL status are removed and your LEFT JOIN behaves like an INNER JOIN. Put conditions on the right table inside the `ON`, or use `IS NULL` on purpose.
2. **Row multiplication.** If the right table has many matches per key, the left rows repeat. Then `COUNT(*)` or `SUM` is too big. Before you join, ask: how many rows per key on each side? Aggregate first in a subquery when needed.
3. **Ambiguous or wrong key.** Forgetting the `ON` gives a cross join with millions of rows. Joining on the wrong column gives plausible but wrong numbers. Always read the join back: "an order belongs to one restaurant, so I join on restaurant_id".

## Say it like this

"I join orders to restaurants on restaurant_id, so each order gets its city. I use an inner join because every order has a restaurant. For customers with no orders I use a left join and filter where the order id is null, or NOT EXISTS, which is safe with NULLs. Before aggregating I check that the join does not multiply rows, because a one-to-many join would inflate my counts."
