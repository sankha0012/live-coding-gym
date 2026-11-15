**Why this matters.** If a feature is nearly a copy of the label, a model will look brilliant in testing and fail in real life, because that feature uses information we will not have at prediction time. A quick correlation scan is the cheap first filter for this.

**How we get there.**
1. `features.corrwith(label)` computes the Pearson correlation of every column with the label and returns one number per column.
2. Take `.abs()`. A feature that is almost the negative of the label leaks just as badly, so the sign must not matter.
3. Compare with the threshold, strictly: `corr > threshold`. Then `corr.index[...]` picks the column names that pass.
4. Return `sorted(...)` of those names, so the result is a plain, ordered list.

A constant column has an undefined correlation, which comes out as NaN. NaN is never greater than anything, so such a column is not flagged without any special code.

**Check it.** No columns gives an empty list, and so does a case where nothing passes. The cost is proportional to rows times columns.

**Watch out.** Forgetting `abs()` misses strong negative leaks, and using `>=` instead of `>` flags columns that sit exactly on the threshold.
