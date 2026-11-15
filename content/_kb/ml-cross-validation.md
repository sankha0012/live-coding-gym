---
title: Cross-validation
summary: Estimate model quality by training and scoring on several different splits of the same data.
tags: [machine learning, scikit-learn, validation]
---
```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=200, n_features=4, random_state=0)
pipe = make_pipeline(StandardScaler(), LogisticRegression())
scores = cross_val_score(pipe, X, y, cv=5)       # [0.875, 1.0, 1.0, 0.925, 0.925]  accuracy per fold
scores.mean(), scores.std()                      # (0.945, 0.048)
cross_val_score(pipe, X, y, cv=5, scoring="roc_auc").mean()   # 0.987
```

- With `cv=5` the data is cut into 5 folds. Each fold is the test set once and training data four times.
- Report the mean and the spread across folds, not the best fold.
- Pass a pipeline so preprocessing is refitted inside every fold.

<!-- more -->

## Details

`cross_val_score` clones the estimator for each fold, so your `pipe` object is left unfitted. Fit it yourself afterwards on the full training data.

For a classifier, an integer `cv` uses `StratifiedKFold` without shuffling. For a regressor it uses plain `KFold`. Pass a splitter object to control it:

```python
from sklearn.model_selection import StratifiedKFold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
cross_val_score(pipe, X, y, cv=cv, scoring="f1").mean()    # 0.946
```

What the splitters do, on six rows:

```python
import numpy as np
from sklearn.model_selection import GroupKFold, KFold
[test for _, test in KFold(n_splits=3).split(np.arange(6))]
# [0 1], [2 3], [4 5]   contiguous blocks, in order
groups = np.array([1, 1, 2, 2, 3, 3])
[test for _, test in GroupKFold(n_splits=3).split(np.arange(6), groups=groups)]
# [4 5], [2 3], [0 1]   a group is never split between train and test
```

- `StratifiedKFold` keeps the class ratio in each fold. Use it for imbalanced labels.
- `GroupKFold` keeps all rows of one customer or one user together.
- `TimeSeriesSplit` always trains on the past and tests on the future.

`cross_validate` returns a dict and takes several metrics:

```python
from sklearn.model_selection import cross_validate
res = cross_validate(pipe, X, y, cv=5, scoring=["accuracy", "roc_auc"])
sorted(res)      # ['fit_time', 'score_time', 'test_accuracy', 'test_roc_auc']
```

`GridSearchCV(pipe, param_grid, cv=5)` runs cross-validation for every parameter combination and refits the best one. Its `best_score_` is slightly optimistic, because the parameters were chosen on those same folds. Keep a final test set that the search never touches.

Error metrics are negated so that higher is always better: `scoring="neg_mean_absolute_error"`.

## Common mistakes

- Scaling, imputing or selecting features on all the data before cross-validating. Put those steps in the pipeline.
- Using plain `KFold` without shuffle on data sorted by label or by time.
- Splitting rows of the same customer across folds, so the model is tested on people it has seen.
- Using shuffled folds on time series.
- Reporting the cross-validation score of the tuned model as the final test score.

## See also

- [scikit-learn Pipeline](#/kb/ml-sklearn-pipeline)
- [Train/test splits and data leakage](#/kb/ml-train-test-split-leakage)
- [Time-based splits and leakage](#/kb/pd-time-split-leakage)
- Official docs: https://scikit-learn.org/stable/
