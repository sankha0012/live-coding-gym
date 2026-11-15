**Why this matters.** Real data has holes, and every preparation step learns numbers from the data. If we do these steps by hand, it is easy to learn them from the wrong rows. One pipeline keeps it all together.

**How we get there.**
1. Use `Pipeline`, a list of `(name, estimator)` pairs. The data flows through them in list order.
2. Put `SimpleImputer(strategy="median")` first. The scaler and the classifier cannot handle `NaN`, so the holes must be filled before they see anything. The median is less affected by outliers than the mean.
3. Next comes `StandardScaler`, which now gets complete numbers.
4. Last is `LogisticRegression(random_state=0)` as the final model.
5. Give each step a clear name, like `impute`, `scale` and `model`, so we can read fitted values later. Return it without fitting, so each call is a fresh object.

**Check it.** One `fit` call learns the median, the mean and the weights from the training data only, and `predict` reuses them. Cost grows linearly with rows and columns.

**Watch out.** With the scaler before the imputer the `NaN` values break the pipeline, and with no imputer at all `fit` fails on missing values.
