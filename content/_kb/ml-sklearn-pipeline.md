---
title: scikit-learn Pipeline
summary: Chain preprocessing steps and a model into one object that fits and predicts as a unit.
tags: [machine learning, scikit-learn, pipeline]
---
```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=200, n_features=4, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
pipe = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
pipe.fit(X_train, y_train)          # fits the scaler, transforms, then fits the model
pipe.predict(X_test[:3])            # array([0, 0, 0])
pipe.score(X_test, y_test)          # 0.96  accuracy
```

- Steps are `(name, estimator)` tuples. Every step but the last must be a transformer.
- `fit` learns each step on the training data only. `predict` reuses what was learned.
- Reach a step's parameter with `stepname__param`, with two underscores.

<!-- more -->

## Details

`pipe.fit(X, y)` calls `fit_transform` on each transformer in order and `fit` on the last step. `pipe.predict(X)` calls `transform` on each transformer, then `predict`. The scaler therefore never sees test rows when it learns its mean and standard deviation. That is the main reason to use a pipeline: it removes a whole class of leakage.

The pipeline has the methods of its last step: `predict`, `predict_proba`, `score`.

Inspecting a fitted pipeline:

```python
pipe.named_steps["model"].coef_.shape    # (1, 4)
pipe.named_steps["scale"].mean_          # the 4 training means
pipe[:-1].transform(X_test[:1])          # the row as the model sees it
```

`make_pipeline` builds the same thing and names the steps after the lowercased class:

```python
from sklearn.pipeline import make_pipeline
auto = make_pipeline(StandardScaler(), LogisticRegression())
[name for name, _ in auto.steps]         # ['standardscaler', 'logisticregression']
```

Set or search parameters through the step name:

```python
from sklearn.model_selection import GridSearchCV
pipe.set_params(model__C=0.1)
search = GridSearchCV(pipe, {"model__C": [0.01, 0.1, 1, 10]}, cv=5).fit(X_train, y_train)
search.best_params_                      # {'model__C': 1}
round(search.best_score_, 3)             # 0.953
```

Because the whole pipeline is refitted inside each fold, the cross-validation score is honest.

A pipeline is a single object, so one `joblib.dump` saves the preprocessing and the model together.

## Common mistakes

- Scaling or imputing the whole dataset before the split, outside the pipeline.
- Calling `fit` or `fit_transform` on the test set. On test data you only `predict` or `transform`.
- Writing `{"C": [1, 10]}` in a grid search over a pipeline. It raises `ValueError: Invalid parameter 'C'`. Use `model__C`.
- Putting the model before a transformer. Only the last step may be a plain estimator.
- Saving the model but not the scaler, then predicting on unscaled data.

## See also

- [ColumnTransformer and encoders](#/kb/ml-column-transformer)
- [Cross-validation](#/kb/ml-cross-validation)
- [Train/test splits and data leakage](#/kb/ml-train-test-split-leakage)
- [Saving and loading models with joblib](#/kb/ml-joblib-persistence)
- Official docs: https://scikit-learn.org/stable/
