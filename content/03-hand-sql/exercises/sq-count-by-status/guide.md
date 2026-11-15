**Why this matters.** Counting rows per category is the first thing we do with any new table: it tells us what the data looks like. The only subtlety is making the output order reproducible.

**How we get there.**
1. Pick the table: `FROM orders`.
2. Collapse rows into one group per status with `GROUP BY status`.
3. Count the rows in each group with `COUNT(*)` and call it `n`. Every selected column is either in the GROUP BY or inside an aggregate; that is the rule SQL enforces.
4. Sort with `ORDER BY n DESC` so the biggest group comes first.
5. Add `status` as a second sort key, so groups with the same count always come out in the same order.

**Check it.** The whole query is `SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY n DESC, status`. It reads the table once, so the cost is linear.

**Watch out.** Forgetting the tie-breaker gives an order that may change between runs when two statuses have the same count.
