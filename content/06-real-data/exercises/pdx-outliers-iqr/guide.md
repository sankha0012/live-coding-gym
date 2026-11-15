**Why this matters.** Before trusting an average, we want to know whether a few huge or tiny values are pulling it. The IQR rule is a robust way to flag them, because quartiles are not dragged around by the extremes the way the mean and standard deviation are.

**How we get there.**
1. Take the `subtotal` column. If it has no known values, return `[]` right away, since quartiles of nothing are undefined.
2. `s.quantile(0.25)` and `s.quantile(0.75)` give Q1 and Q3. Missing values are skipped, so they cannot shift the quartiles.
3. The spread is `iqr = q3 - q1`, and the fences are `q1 - 1.5 * iqr` and `q3 + 1.5 * iqr`.
4. Build one mask: `(s < low) | (s > high)`. The strict signs mean a value exactly on a fence is not flagged.
5. Take `order_id` where the mask is true, convert each to `int`, and sort.

**Check it.** A missing subtotal compares as False on both sides, so it is never flagged. The cost is O(n log n) for the quantiles.

**Watch out.** Dropping the missing rows from the frame before taking ids, or using `<=`, changes which orders get flagged.
