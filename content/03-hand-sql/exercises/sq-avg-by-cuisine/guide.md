**Why this matters.** An average looks simple, but it silently depends on which rows enter it. Here two things decide the number: cancelled orders must not count, and missing subtotals must not count as zero.

**How we get there.**
1. The cuisine lives on the restaurant, not on the order, so we join: `orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id`.
2. Keep only delivered orders with `WHERE o.status = 'delivered'`. WHERE runs before the groups are built, so cancelled orders never reach the average.
3. Group the remaining rows with `GROUP BY r.cuisine`, one group per cuisine.
4. Take `AVG(o.subtotal)`. AVG ignores NULL values, which is exactly what the problem asks for.
5. Round the result once, at the end, with `ROUND(..., 2)`, then sort by cuisine.

**Check it.** A NULL subtotal is left out of both the sum and the count, so the average is over the orders that have a value. The cost is a single pass over the orders plus the grouping.

**Watch out.** Writing `AVG(COALESCE(subtotal, 0))` feels safe but drags every average down.
