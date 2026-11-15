**Why this matters.** Orders without a coupon have NULL in `coupon_code`, and NULL behaves like nothing: it equals nothing, not even itself. We have to give those orders a name before we count them as a group.

**How we get there.**
1. Turn NULL into a label: `COALESCE(coupon_code, 'none') AS coupon`. It returns the first value that is not NULL.
2. `GROUP BY coupon` puts all the no-coupon orders together in one group called `'none'`.
3. `COUNT(*)` gives the orders per coupon.
4. For the share, divide by the total: `100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders)`. The subquery gives one number for the whole table, and `100.0` forces decimal division.
5. `ORDER BY n DESC`.

**Check it.** The percentages add up to 100. Every order is counted, whatever its status. The cost is two scans.

**Watch out.** Dividing integers, which rounds each share down, or forgetting `COALESCE` so the no-coupon orders show up with a NULL label.
