**Why this matters.** "Share of the total" needs two levels of aggregation: a number per restaurant and a number per city. Doing both in one query gets tangled, so we build the answer in layers.

**How we get there.**
1. First CTE `rev`: join `orders` to `restaurants`, keep delivered orders, and `GROUP BY r.city, o.restaurant_id` with `SUM(o.subtotal)` as `revenue`. The city comes from the restaurant, as asked.
2. Second CTE `city_total`: add up the rows of `rev` per city. It reads the first CTE, not the raw table.
3. Join `rev` to `city_total` on city. Now each restaurant row sits next to its city's total.
4. Compute `rev.revenue * 1.0 / ct.total`. The `* 1.0` forces decimal division instead of whole-number division.
5. Keep rows where that share is above 0.2, round to 3 decimals for display, and sort.

**Check it.** A city with a single restaurant has a share of 1.0, so it always appears. Each CTE can be run alone to check it.

**Watch out.** Without `* 1.0`, integer-looking values can divide as whole numbers and the shares collapse to 0.
