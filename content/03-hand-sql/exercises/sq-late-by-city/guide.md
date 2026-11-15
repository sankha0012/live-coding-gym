**Why this matters.** A KPI such as "late deliveries" needs a precise definition before we can count it. Here late means actual time above the promise, and it only makes sense for orders that were delivered.

**How we get there.**
1. The city is on the restaurant, so join `orders o` to `restaurants r`.
2. Keep delivered orders with `o.status = 'delivered'`. Cancelled orders have no `actual_minutes`, so they cannot be late.
3. Add the definition of late: `o.actual_minutes > o.promised_minutes`. Both conditions go in WHERE, because they remove rows.
4. `GROUP BY r.city` and `COUNT(*)` as `late_orders`.
5. Sort by `late_orders DESC, r.city` so ties are stable.

**Check it.** A comparison with NULL is never true, so cancelled orders would drop out anyway, but the status filter states the intent. A city with no late orders does not appear. The cost is one pass.

**Watch out.** Using `>=` counts on-time orders as late; the problem says strictly above.
