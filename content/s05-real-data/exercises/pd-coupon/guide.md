**Why this matters.** Someone asks whether coupons raise order value. Computing two means is easy. The real skill is knowing what the answer does and does not prove.

**How we get there.**
1. Keep only delivered orders and copy them. Cancelled orders are not real purchases, so they would pollute both means.
2. Build a True/False column from the coupon code: `d["coupon_code"].notna()`. The code is missing when no coupon was used.
3. Group by that column and take the mean of `subtotal`. Now one group is with a coupon and the other without, in a single step.
4. Pull out `means[True]` and `means[False]`, round each to 2 decimals, and return them as a tuple of floats.

**Check it.** Pandas `mean` skips missing subtotals, which is what we want. Filling them with 0 would drag both means down. One pass over the data.

**Watch out.** Counting cancelled orders, or turning missing subtotals into zero, both shift the means. And a gap between the groups is only a correlation: coupons might go to a different kind of customer, who may order differently anyway. Proving a cause needs a randomised test.
