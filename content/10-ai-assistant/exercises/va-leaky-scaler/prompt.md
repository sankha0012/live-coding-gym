An AI assistant wrote this. The tests fail. Find the bug and fix it with the smallest safe change.

`prepare(X, y, seed)` splits the data with `train_test_split(X, y, test_size=0.25, random_state=seed)` and standardises the features with a `StandardScaler`. It returns `(X_train_s, X_test_s, y_train, y_test, scaler)`. The scaler must learn its mean and scale from the training rows only. The test rows are transformed with that same scaler, never used to fit it. The result must be the same every time for the same `seed`.
