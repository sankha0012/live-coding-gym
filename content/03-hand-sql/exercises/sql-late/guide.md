**Why this matters.** A late rate tells you which kinds of restaurants break their promise. The danger is deciding who is in the denominator: only orders that actually arrived can be late.

**How we get there.**
1. Join `orders` to `restaurants` to get the cuisine.
2. Keep only delivered orders with `WHERE o.status = 'delivered'`. Cancelled orders have no `actual_minutes`, so they cannot be late or on time.
3. `GROUP BY r.cuisine`.
4. Make a 0/1 indicator: `CASE WHEN o.actual_minutes > o.promised_minutes THEN 1.0 ELSE 0 END`.
5. Take the `AVG` of it, which is the late share per cuisine, then `ORDER BY late_rate DESC`.

**Check it.** The average of an indicator is a rate between 0 and 1. The cost is one scan and a group.

**Watch out.** Skipping the delivered filter: a cancelled order has a NULL time, the comparison is not true, so the `CASE` counts it as not late and the rate drops.
