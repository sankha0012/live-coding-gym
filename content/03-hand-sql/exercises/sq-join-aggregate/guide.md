**Why this matters.** Most business questions are "total of X per Y" where Y lives in another table. We join to bring Y in, then aggregate.

**How we get there.**
1. The cuisine is on restaurants, so `FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id`.
2. Remove cancelled orders with `WHERE o.status = 'delivered'`. This removes rows, so it belongs before grouping, in WHERE.
3. Group by `r.cuisine`.
4. For each group, `COUNT(*)` gives the orders and `ROUND(SUM(o.subtotal), 2)` gives the revenue.
5. Sort by `revenue DESC`, then `r.cuisine` to break ties.

**Check it.** `SUM` skips NULL subtotals, so a missing value does not break the total. The cost is one pass plus a small sort of the groups.

**Watch out.** Putting the status filter in HAVING, or forgetting it, mixes cancelled orders into the revenue.
