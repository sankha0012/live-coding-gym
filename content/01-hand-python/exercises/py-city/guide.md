**Why this matters.** This is a SQL GROUP BY done by hand. The details that bite are the filter (only delivered orders) and a missing subtotal that must count as zero instead of crashing the addition.

**How we get there.**
1. Start with an empty dict `out` that will hold a running total per city.
2. Loop over the orders and skip any whose status is not `"delivered"`, which is our WHERE.
3. Add to the city's total: `out.get(city, 0) + (o["subtotal"] or 0) + o["fee"]`. The `.get` with a default of 0 starts a new city, and `or 0` turns a None subtotal into 0.
4. Round only at the end, `{c: round(v, 2) for c, v in out.items()}`, so rounding errors do not pile up while we add.

**Check it.** An empty list gives `{}`. A city with only cancelled orders never appears. One pass, linear time.

**Watch out.** Adding `o["subtotal"]` directly raises a TypeError when it is None, and forgetting the status filter counts cancelled orders in GMV.
