Write `cv_accuracy(X, y) -> float` that returns the mean accuracy of 5-fold stratified cross validation.

- The model is a `Pipeline` of `StandardScaler` then `LogisticRegression(max_iter=1000, random_state=0)`. The scaler must be inside the pipeline, so each fold learns its scaling from its own training part only. Never scale `X` before the split.
- The folds come from `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`.
- Use `accuracy` scoring and return the mean of the five fold scores as a plain Python `float` (not a numpy float).
- `X` can be a numpy array or a DataFrame. Do not change `X` or `y`.

Calling it twice with the same input gives the same number.
