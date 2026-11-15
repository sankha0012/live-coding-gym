**Why this matters.** A summary table per group is the bread and butter of data work, and the details decide whether the numbers are right. Here the hidden detail is the difference between counting rows and counting known values.

**How we get there.**
1. Orders do not know their city or cuisine, so `orders.merge(restaurants, on="restaurant_id", how="inner")` brings them in. An inner join also drops orders whose restaurant is unknown, which is what we want.
2. Group by both columns: `m.groupby(["city", "cuisine"])`.
3. Use named aggregations: `orders=("order_id", "size")` and `avg_subtotal=("subtotal", "mean")`. `size` counts rows, so an order with a missing subtotal still counts, while `mean` skips the missing values.
4. `reset_index()` turns the group keys back into columns, then `round(2)` on the mean.
5. Sort by `["orders", "city", "cuisine"]` with `ascending=[False, True, True]`, then `reset_index(drop=True)`. The two tie breakers make the order fully determined.

**Check it.** No orders gives an empty frame with the same columns. The cost is one merge and one grouping pass.

**Watch out.** Counting with `count` on `subtotal` silently skips orders with a missing subtotal.
