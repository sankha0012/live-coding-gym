Write `build_model() -> Pipeline` that returns an unfitted scikit-learn `Pipeline` with exactly three steps, in this order:

1. `SimpleImputer` with `strategy="median"`.
2. `StandardScaler`.
3. `LogisticRegression` with `random_state=0`.

The pipeline must fit and predict on a numeric array that contains `NaN`. Every call returns a new pipeline object. Do not fit it inside the function.
