**Why this matters.** The column name an assistant picks is a claim. Here the alias says "delivered" but nothing in the query enforces it.

**How we get there.**
1. Run the query and pick a restaurant, for example restaurant 8.
2. Run `SELECT status, COUNT(*) FROM orders WHERE restaurant_id = 8 GROUP BY status`. It shows 110 in the result, which is 100 delivered plus 10 cancelled.
3. Cause: no row filter on status. HAVING runs after grouping and only sees the group count.
4. Add `WHERE status = 'delivered'` before `GROUP BY`. WHERE removes rows, HAVING removes groups.
5. Keep `HAVING COUNT(*) > 100` and the same ORDER BY.

**Check it.** Counts in the result equal the delivered count you get by hand, and restaurant 8 drops out of the list.

**Watch out.** The threshold is strictly more than 100, so a restaurant with exactly 100 delivered orders stays out.
