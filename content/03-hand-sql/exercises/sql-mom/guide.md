**Why this matters.** Growth is a comparison with the previous period. In SQL, comparing a row with the row before it is what `LAG` is for.

**How we get there.**
1. In a CTE, label each order with its month using `strftime('%Y-%m', created_at)`.
2. Keep delivered orders, `GROUP BY month` and `COUNT(*)`. Now we have one row per month.
3. Over those rows, `LAG(orders) OVER (ORDER BY month)` returns the previous month's count. The `ORDER BY` inside the window defines what "previous" means.
4. Subtract it: `orders - LAG(orders) OVER (ORDER BY month)`.
5. `ORDER BY month`.

**Check it.** The first month has no previous row, so `LAG` returns NULL and so does the difference. That is correct, not a bug. The cost is one group and one sort. In other databases we would use `DATE_TRUNC('month', ...)` instead of `strftime`.

**Watch out.** Computing `LAG` before grouping, which compares one order with the one before it, not one month with the previous month.
