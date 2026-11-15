**Why this matters.** Sometimes one number must be compared with a statistic of the same numbers, such as restaurants above the average restaurant. A CTE lets us compute the per-restaurant figure once and use it twice.

**How we get there.**
1. Name step one: `WITH rev AS (...)`. Inside, filter delivered orders, `GROUP BY restaurant_id`, and compute `ROUND(SUM(subtotal), 2) AS revenue`.
2. Now `rev` is a small table with one row per restaurant, so we can query it like any table.
3. The average we need is over those rows: `(SELECT AVG(revenue) FROM rev)`. This is a scalar subquery that returns one value.
4. Keep rows with `WHERE revenue > (SELECT AVG(revenue) FROM rev)`.
5. Sort by `revenue DESC, restaurant_id`.

**Check it.** Restaurants without a delivered order are not in `rev`, so they do not pull the average down, as the problem states. The cost is one scan of `orders` plus a tiny pass over `rev`.

**Watch out.** Averaging the order subtotals instead gives the average order, not the average restaurant.
