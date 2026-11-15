**Why this matters.** Sometimes a row has to be compared with a number computed from the whole table, like the average. A scalar subquery gives us that number inside the filter.

**How we get there.**
1. First write the benchmark on its own: `SELECT AVG(subtotal) FROM orders WHERE status = 'delivered'`. It returns exactly one value.
2. In the outer query, select `order_id` and `subtotal` from `orders` with `WHERE status = 'delivered'`.
3. Add `AND subtotal > 2 * (...)` and paste the benchmark query in the parentheses. Because it returns one value, it works like a constant.
4. `ORDER BY order_id`.

**Check it.** The inner query does not depend on the outer row, so it needs only one pass, and the whole thing is two scans, O(n). The average is the same for every row, so it is not recomputed per row.

**Watch out.** Leaving the `status` filter out of the inner query: cancelled orders would then pull the average and change who counts as far above it.
