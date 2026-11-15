**Why this matters.** Filtering happens at two different moments in a query, and picking the wrong one is a frequent error. We filter rows, and we also filter groups by their size.

**How we get there.**
1. Start with `FROM orders` and keep only delivered rows: `WHERE status = 'delivered'`. WHERE works on single rows, before any grouping.
2. Group by restaurant: `GROUP BY restaurant_id`, and count with `COUNT(*) AS delivered_orders`.
3. Now we want only large groups. The count does not exist until grouping is done, so we cannot use WHERE. We use `HAVING COUNT(*) > 100`, which filters groups.
4. Sort by `delivered_orders DESC, restaurant_id` so ties are stable.

**Check it.** The rule is strictly more than 100, so a restaurant with exactly 100 is out. The query scans the table once, so it is linear.

**Watch out.** Writing `WHERE COUNT(*) > 100` is an error, and moving the status filter into HAVING would count cancelled orders too.
