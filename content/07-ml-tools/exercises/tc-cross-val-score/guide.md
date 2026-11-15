**Why this matters.** The easy way to score a model is to scale everything first and cross-validate afterwards. That leaks information from the test folds into training, and the score looks better than reality.

**How we get there.**
1. Put the steps in one `Pipeline`: `StandardScaler` then `LogisticRegression(max_iter=1000, random_state=0)`. The scaler now belongs to the model.
2. Build the splitter, `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`. Stratified keeps the class ratio in each fold, and the fixed seed makes the result repeat. Without shuffling, a sorted dataset gives folds with different classes.
3. Hand the whole pipeline to `cross_val_score` with that splitter and `scoring="accuracy"`. For every fold it refits the scaler on the training part only.
4. Take the mean and wrap it in `float(...)`, because `scores.mean()` is a numpy float and the spec wants a plain one.

**Check it.** This works for arrays and DataFrames and does not change them. The cost is five model fits.

**Watch out.** Scaling `X` before the split is the leak this exercise is built to catch, and returning the array of scores instead of the mean is the other easy slip.
