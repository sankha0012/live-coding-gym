**Why this matters.** The same feature is computed in two places, for training and for serving, and over time they drift apart. The model then sees inputs it never learned, and nothing crashes.

**How we get there.**
1. Reproduce. Feed one row to both functions, including a missing amount and a messy category like `" Food "`, and compare field by field.
2. Locate the differences. Serving uses `log` where training uses `log1p`. It does not treat a missing amount as 0.0, and it skips the `strip`, `lower` and the "unknown" default for the category.
3. We could patch each one, but that keeps two copies of the logic, ready to drift again.
4. Instead make serving call the training code on a one-row list: `train_features([row], stats)[0]`. There is now one source of truth, and `train_features` is untouched.

**Check it.** The cost per row is the same small constant work plus a one-element list. The paths now agree, including on missing values.

**Next time.** When a feature has two implementations, compare them on edge cases and share the code.

**Watch out.** Fixing only the amount or only the category leaves half the skew.
