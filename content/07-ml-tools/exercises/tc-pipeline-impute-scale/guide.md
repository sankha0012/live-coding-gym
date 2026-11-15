**Why this matters.** Real data has holes, and every preparation step learns numbers from the data. If we do these steps by hand, it is easy to learn them from the wrong rows. One pipeline keeps it all together.

**How we get there.**
1. Use `Pipeline`, a list of `(name, estimator)` pairs. The data flows through them in list order.
2. Put `SimpleImputer(strategy="median")` first. `LogisticRegression` refuses `NaN`, and the scaler only passes it through, so the holes must be filled before the imputer's median can be learned from raw values.
3. Next comes `StandardScaler`, which now gets complete numbers.
4. Last is `LogisticRegression(random_state=0)` as the final model.
5. Give each step a clear name, like `impute`, `scale` and `model`, so we can read fitted values later. Return it without fitting, so each call is a fresh object.

**Check it.** One `fit` call learns the median, the mean and the weights from the training data only, and `predict` reuses them.

**Watch out.** With the scaler before the imputer, `fit` still runs, but the imputer learns its median from rescaled numbers, so the stored median is not the real one. With no imputer at all, `fit` fails on missing values.
