**Why this matters.** A join can silently go wrong. If the lookup table has the same key twice, every matching row on the left is repeated, and every later sum or count is inflated with no error at all. A cheap check right after the join catches it.

**How we get there.**
1. Use a left merge: `orders.merge(restaurants, on="restaurant_id", how="left")`. Every order keeps its row, and orders with no restaurant get NaN in the new columns. The row order follows `orders`.
2. Compare the sizes: `len(merged) != len(orders)`.
3. If they differ, `raise ValueError(...)` with both counts in the message, so whoever reads the error sees how much the join changed.
4. Otherwise return the merged frame as it is.

We raise instead of cleaning up, because a half-fixed frame hides the real problem, which is a duplicate key in the data.

**Check it.** Orders without a matching restaurant are fine, since they do not change the count. Zero orders merge to zero rows. The check costs nothing extra.

**Watch out.** Returning the merged frame without comparing counts passes every normal case and fails exactly when the data is dirty.
