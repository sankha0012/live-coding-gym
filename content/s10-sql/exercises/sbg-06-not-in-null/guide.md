**Why this matters.** `NOT IN` with a nullable column is one of the classic silent SQL failures: no error, just an empty or too-small result.

**How we get there.**
1. Run the query. It returns no rows, which is suspicious for a city with many customers.
2. Run the subquery alone: `SELECT customer_id FROM orders WHERE status = 'delivered'`. One value is NULL.
3. Cause: `customer_id NOT IN (..., NULL)` is never true, because every comparison with NULL is unknown.
4. Rewrite with `NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'delivered')`. A NULL key just never matches.
5. Keep the city filter and the ORDER BY.

**Check it.** The result is not empty, and it includes customers whose orders are all cancelled.

**Watch out.** Adding `WHERE customer_id IS NOT NULL` inside the NOT IN subquery also works, but NOT EXISTS is safer because it does not depend on remembering that.
