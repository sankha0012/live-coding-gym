**Why this matters.** A running total shows how a number builds up over time, like revenue so far this week. We need one row per day, so we first collapse the orders, and only then accumulate.

**How we get there.**
1. In a CTE, filter delivered orders in the date range with `date(created_at) BETWEEN '2026-10-01' AND '2026-10-07'`. Using `date()` keeps the whole last day in.
2. `GROUP BY date(created_at)` and `SUM(subtotal)` gives the revenue per day.
3. Over those daily rows, add `SUM(revenue) OVER (ORDER BY day)`. With an `ORDER BY` and no explicit frame, the window sums from the first row up to the current one.
4. Round both columns to 2 decimals at the very end, so floating-point noise does not show.
5. `ORDER BY day`.

**Check it.** Summing the raw orders in the window would give a running total per order, not per day. The cost is one group and one sort.

**Watch out.** Comparing `created_at` to `'2026-10-07'` directly, which loses that day's orders (the timestamps are all later than the bare date text). Rounding the daily revenue before the running sum can also let cent errors pile up.
