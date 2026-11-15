**Why this matters.** "Top N per group" is a daily task: the best two restaurants in every city. A plain `LIMIT` would cut the whole result once, not once per city.

**How we get there.**
1. In a CTE, join `orders` to `restaurants`, keep delivered orders, and `GROUP BY r.city, o.restaurant_id` with `SUM(o.subtotal)` as `revenue`.
2. Number the restaurants inside each city: `ROW_NUMBER() OVER (PARTITION BY city ORDER BY revenue DESC)`. `PARTITION BY` restarts the count for each city, and the biggest revenue gets 1.
3. A window result cannot be filtered in the same `SELECT`, so we put it in a subquery.
4. Outside, keep `WHERE rn <= 2`.
5. `ORDER BY city, rn`.

**Check it.** A city with only one restaurant simply gives one row. The cost is one group and one sort.

**Watch out.** `ROW_NUMBER` breaks ties arbitrarily, so two restaurants with equal revenue at the cut could swap. If ties matter, we choose `RANK` or add a tie-break and say the rule.
