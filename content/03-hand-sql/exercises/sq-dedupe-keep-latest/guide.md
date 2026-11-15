**Why this matters.** Duplicated records are everywhere: many orders per customer and restaurant, but we want only the latest. We cannot do it with a simple GROUP BY, because we need the whole row, not just the date.

**How we get there.**
1. Narrow the data first: `FROM orders WHERE customer_id <= 5`.
2. Number the rows inside each pair: `ROW_NUMBER() OVER (PARTITION BY customer_id, restaurant_id ORDER BY created_at DESC, order_id DESC) AS rn`. The newest order of each pair gets 1.
3. The second sort key, `order_id DESC`, settles ties on `created_at`, so the winner is always the same.
4. We cannot filter on a window function in the same SELECT, so we wrap this query in an outer one.
5. The outer query keeps `WHERE rn = 1` and sorts by customer and restaurant.

**Check it.** Exactly one row per pair survives, even with ties. The window sorts each partition, so the cost is O(n log n).

**Watch out.** `GROUP BY` with `MAX(created_at)` loses the other columns, and joining back on the date can return ties twice.
