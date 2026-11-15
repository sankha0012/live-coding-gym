**Why this matters.** `COUNT(col)` skips NULLs on its own. Adding a WHERE to "handle NULLs" changes which rows exist for every other aggregate in the same query.

**How we get there.**
1. Run the query. The prompt asks for counts per status, and there are two statuses, but you get one row.
2. Check `SELECT status, COUNT(*) FROM orders GROUP BY status` to see what the totals should be.
3. Find the cause: `WHERE actual_minutes IS NOT NULL`. Every cancelled order has a NULL there, so the whole group is filtered out before grouping.
4. Remove the WHERE. `COUNT(actual_minutes)` already counts only non-NULL values, and `COUNT(*)` counts all rows.
5. Run again and compare with the reference.

**Check it.** Both statuses appear, and `total_orders` summed over the statuses equals the number of rows in orders.

**Watch out.** If you want "count only some rows" for one column and not the others, use `COUNT(CASE WHEN ... THEN 1 END)` or `SUM(condition)` instead of a WHERE.
