**Why this matters.** Real reports slice data by more than one thing at once, such as city and cuisine. The idea is that a group is a distinct combination of values, not one column.

**How we get there.**
1. City and cuisine live on `restaurants`, and the orders live on `orders`. So we join them on `restaurant_id`.
2. Keep only delivered orders with `WHERE o.status = 'delivered'`. Filtering rows before grouping is cheaper and clearer.
3. `GROUP BY r.city, r.cuisine`. Each distinct pair becomes one group.
4. `COUNT(*)` counts the orders inside each group.
5. `ORDER BY r.city, r.cuisine` so the output is in a fixed order.

**Check it.** A pair with no delivered orders never has rows, so it cannot show up, which is what the problem wants. Every selected column is either in the `GROUP BY` or inside an aggregate. The cost is linear in the orders.

**Watch out.** Grouping by only one of the two columns, or selecting a column that is neither grouped nor aggregated. SQLite does not raise an error for that; it silently returns the value from an arbitrary row of the group, which is worse.
