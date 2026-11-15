**Why this matters.** COUNT looks like one function but it is really two. Mixing them up gives wrong numbers with no error, which is the worst kind of bug in a report.

**How we get there.**
1. Group the orders by status: `FROM orders GROUP BY status`.
2. `COUNT(*)` counts every row in the group. That is `total_orders`.
3. `COUNT(coupon_code)` counts only rows where `coupon_code` is not NULL. That is `with_coupon`, with no extra WHERE needed.
4. `COUNT(actual_minutes)` does the same for the delivery time. Cancelled orders have no time, so their `with_actual` is 0.
5. Sort by status.

All three counts come from the same scan, side by side.

**Check it.** The three numbers differ exactly when NULLs are present, so `with_actual` below `total_orders` is expected, not a bug. The cost is one pass.

**Watch out.** Using `COUNT(col)` as if it counted rows silently drops every row where that column is NULL.
