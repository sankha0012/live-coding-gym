---
title: Train/test splits and data leakage
summary: Hold out a test set with train_test_split and keep every bit of test information out of training.
tags: [machine learning, scikit-learn, leakage]
---
```python
import numpy as np
from sklearn.model_selection import train_test_split

X = np.arange(20).reshape(10, 2)
y = np.array([0] * 8 + [1] * 2)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0)       # shapes (8, 2) and (2, 2)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.5, random_state=0, stratify=y)
y_train.sum(), y_test.sum()                    # (1, 1)  one positive on each side
```

- The return order is `X_train, X_test, y_train, y_test`.
- `random_state` makes the split repeatable. `stratify=y` keeps the class ratio on both sides.
- Fit everything (scalers, imputers, encoders, feature selection) on the training set only.

<!-- more -->

## Details

Without `stratify`, the same 50/50 split with `random_state=0` puts both positives in the test set and none in training. With rare classes, always stratify.

`train_test_split` also accepts a DataFrame and returns two frames: `train, test = train_test_split(df, test_size=0.3, random_state=42)`.

For a validation set, split twice:

```python
X_tr, X_tmp, y_tr, y_tmp = train_test_split(X, y, test_size=0.4, random_state=0)
X_val, X_te, y_val, y_te = train_test_split(X_tmp, y_tmp, test_size=0.5, random_state=0)
len(X_tr), len(X_val), len(X_te)               # (6, 2, 2)
```

Tune on validation. Touch the test set once, at the end.

Leakage is any information in training that will not be available at prediction time. Common sources:

- Preprocessing fitted on all rows before the split.
- A feature that is computed from the target, or only known after the outcome.
- The same customer, or duplicate rows, on both sides of the split.
- Future rows used to predict the past.

Leakage makes scores look good and then fail in production. This example has pure noise features and random labels, so the honest accuracy is about 0.5:

```python
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline

rng = np.random.default_rng(0)
Xn, yn = rng.normal(size=(50, 2000)), rng.integers(0, 2, 50)
X_sel = SelectKBest(f_classif, k=20).fit_transform(Xn, yn)        # selection saw every label
cross_val_score(LogisticRegression(), X_sel, yn, cv=5).mean()     # 0.96  leaked
honest = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression())
cross_val_score(honest, Xn, yn, cv=5).mean()                      # 0.58  selection inside each fold
```

Other splitters: `shuffle=False` takes the last rows as test, for time-ordered data. `GroupShuffleSplit` keeps whole groups on one side.

## Common mistakes

- Unpacking in the wrong order, for example `X_train, y_train, X_test, y_test`.
- Calling `scaler.fit_transform` on the test set. Use `transform`.
- Leaving out `random_state`, so results change on every run.
- Using a random split on time data or on data with repeated customers.
- Looking at the test score many times while tuning. The test set then becomes training data.

## See also

- [scikit-learn Pipeline](#/kb/ml-sklearn-pipeline)
- [Cross-validation](#/kb/ml-cross-validation)
- [Time-based splits and leakage](#/kb/pd-time-split-leakage)
- [Random numbers and seeds](#/kb/py-random-seeds)
- Official docs: https://scikit-learn.org/stable/
