**Why this matters.** A test score is only honest if the test rows are truly unseen. A scaler learns a mean and spread, so if it sees the test rows, information leaks into training and the score looks better than reality.

**How we get there.**
1. Reproduce by asking what each step saw. The buggy code calls `fit_transform` on all of `X` and only then splits, so the scaler's statistics include the test rows.
2. Locate it: the problem is the order of two steps, fit and split.
3. Split first with `train_test_split(X, y, test_size=0.25, random_state=seed)`. The `random_state` keeps the split identical for the same `seed`.
4. Learn the statistics from training rows only: `scaler.fit_transform(X_train)`.
5. Apply them to the test rows with `scaler.transform(X_test)`, which learns nothing new.

**Check it.** The training features now have mean 0, while the test features need not, which is correct.

**Next time.** For every `fit` in a pipeline, ask which rows it saw. Imputers, encoders and feature selectors follow the same rule.

**Watch out.** Fitting a second scaler on the test rows looks tidy, but then train and test use different scales that the model never saw.
