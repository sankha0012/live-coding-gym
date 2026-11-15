**Why this matters.** "What happened next" questions, like time between purchases, need a row to look at the one after it. LEAD does that, the mirror image of LAG.

**How we get there.**
1. Narrow to one customer's delivered orders: `WHERE customer_id = 3 AND status = 'delivered'`. We filter first so cancelled orders are never "next".
2. Define the order in time: `WINDOW w AS (ORDER BY created_at, order_id)`. The `order_id` settles ties.
3. `LEAD(created_at) OVER w` returns the next row's timestamp. The last row has no next one, so it is NULL.
4. To get a gap in days, convert both timestamps with `julianday(...)` and subtract, then `ROUND(..., 1)`.
5. Sort the output with the same keys as the window.

**Check it.** Subtracting NULL gives NULL, so the last order shows NULL in both next columns without special code. The cost is one sort of this customer's orders.

**Watch out.** Filtering by status after computing LEAD would let a cancelled order appear as the "next" one.
