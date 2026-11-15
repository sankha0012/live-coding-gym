**Why this matters.** A rate is a count of something divided by a count of everything. We want that per city, in one pass, without writing two separate queries.

**How we get there.**
1. The city lives on `restaurants`, so we join `orders` to it on `restaurant_id`.
2. `GROUP BY r.city` gives one group per city, and `COUNT(*)` is the number of orders.
3. Turn each order into an indicator: `CASE WHEN o.status = 'cancelled' THEN 1.0 ELSE 0 END` is 1 for a cancellation and 0 otherwise.
4. The average of those 0s and 1s is exactly the share of cancellations, so `AVG(CASE ...)` is the rate as a fraction between 0 and 1.
5. `ORDER BY orders DESC`, using the count alias.

**Check it.** We count all orders, delivered and cancelled, because the rate is out of everything. The cost is one scan and a group.

**Watch out.** Writing the indicator as `1` and `0` only: some databases then divide integers and round the rate down to 0. The `1.0` avoids that.
