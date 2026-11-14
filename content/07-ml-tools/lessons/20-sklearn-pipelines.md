# scikit-learn Pipelines

## What problem it solves

A model is never just a model. Before `fit` you fill missing values, scale numbers and encode categories. If you do these steps by hand in a notebook, three bad things happen.

First, leakage. You compute the mean of a column on the whole dataset, then split. The test rows have now influenced the training step. Your score looks better than the truth.

Second, training and serving drift apart. The notebook scaled the data one way. The service scales it another way, or forgets to. The model gets inputs it never saw.

Third, you cannot save "the model" as one thing. You have a scaler in one file, an encoder in another and a classifier in a third, and you must load them in the right order.

A `Pipeline` fixes all three. It chains the steps into one object. You call `fit` once and `predict` once. Each step learns only from the data you give to `fit`.

## Where it sits in an ML pipeline

It sits between raw tabular data and the prediction. It is the unit you train, evaluate, save and serve. In production the service loads one file and calls `predict` on raw rows. Everything before the model is inside that file, so the service cannot skip a step.

`ColumnTransformer` is the helper for mixed data. It applies one set of steps to the numeric columns and another to the categorical columns, then joins the results.

## A minimal real example

This code runs on Python 3.12 with pandas, numpy and scikit-learn.

```python
import os
import tempfile

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.DataFrame({
    "distance_km": [1.2, 5.0, np.nan, 3.3, 8.1, 2.2, 6.5, np.nan, 4.4, 7.0, 1.0, 9.0],
    "city": ["sp", "rj", "sp", "bh", "rj", "sp", "bh", "rj", "sp", "bh", "rj", "sp"],
    "late": [0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1],
})
X, y = df[["distance_km", "city"]], df["late"]

pre = ColumnTransformer([
    ("num", Pipeline([("imp", SimpleImputer(strategy="median")),
                      ("sc", StandardScaler())]), ["distance_km"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"]),
])
model = Pipeline([("pre", pre), ("clf", LogisticRegression(random_state=0))])

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.25, random_state=0, stratify=y)
model.fit(X_tr, y_tr)                 # median and scale learned on train only
print(model.score(X_te, y_te))        # test rows are only transformed

print(cross_val_score(model, X, y, cv=3))   # refits the whole pipeline per fold

with tempfile.TemporaryDirectory() as d:
    path = os.path.join(d, "model.joblib")
    joblib.dump(model, path)
    again = joblib.load(path)
    print((again.predict(X_te) == model.predict(X_te)).all())   # True
```

Read it in this order. The `ColumnTransformer` handles the two column types. The `Pipeline` adds the classifier. `fit` on the training split learns the median, the scale and the model weights together. `cross_val_score` clones the pipeline and refits it for every fold, so each fold is leak-free. `joblib` saves the whole fitted object to one file.

## The traps

- Fitting a scaler or imputer on all the data before the split. Put the step inside the pipeline instead.
- `handle_unknown="ignore"` on the encoder. Without it, a new city in production raises an error.
- Loading a joblib file made with a different scikit-learn version. It can fail or behave differently. Pin the version, and only load files you trust, because joblib uses pickle.

## What to say in an interview

Say: "I wrap preprocessing and the model in one Pipeline. That way the same steps run in training and in serving, and cross-validation does not leak. I save the fitted pipeline with joblib and pin the library versions."

Say that you use `random_state` so results repeat.

Do NOT claim that a Pipeline makes a model better. It makes the process safer and repeatable. Do NOT say joblib files are safe to load from anyone. Do NOT claim you have tuned hyperparameters with `GridSearchCV` unless you have; just say it takes a pipeline as the estimator.

## Three likely questions

**1. Why use a Pipeline instead of scaling the data first and then calling fit?**
Because scaling first on all rows leaks information from the test set. A Pipeline fits each step on training data only. It also gives one object to save and serve, so training and serving cannot drift.

**2. What does ColumnTransformer do?**
It applies different steps to different columns, for example impute and scale the numbers, one-hot encode the categories. It then joins the outputs into one matrix for the model.

**3. How do you ship the model to production?**
I fit the pipeline on the training data, check it on held-out data, and save it with joblib. The service loads the file once at start-up and calls `predict` on raw rows. I pin the scikit-learn version in the environment, ideally in the container image, so the file loads the same way it was saved.
