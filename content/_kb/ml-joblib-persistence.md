---
title: Saving and loading models with joblib
summary: Write a fitted scikit-learn model or pipeline to disk with joblib.dump and read it back with joblib.load.
tags: [machine learning, joblib, persistence]
---
```python
import joblib
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = make_classification(n_samples=200, n_features=4, random_state=0)
pipe = make_pipeline(StandardScaler(), LogisticRegression()).fit(X, y)
joblib.dump(pipe, "model.joblib")            # returns ['model.joblib']
loaded = joblib.load("model.joblib")         # a fitted Pipeline again
(loaded.predict(X) == pipe.predict(X)).all() # True
```

- Save the whole pipeline, not only the model, so preprocessing travels with it.
- Load with the same scikit-learn version that saved the file.
- Never load a joblib or pickle file from a source you do not trust. Loading runs code.

<!-- more -->

## Details

`joblib.dump(obj, path)` accepts a string or a `pathlib.Path`. `joblib.load(path)` raises `FileNotFoundError` when the file is missing. `compress=3` makes a smaller file and loads the same way.

joblib is pickle with efficient handling of large numpy arrays. It stores the object's state, not the class code. The loading process must be able to import the same classes, so custom transformers have to live in an importable module, not in a notebook cell.

Save the facts you will need at prediction time next to the model. A dict works:

```python
import sklearn
bundle = {
    "model": pipe,
    "features": ["f0", "f1", "f2", "f3"],     # column order used in training
    "threshold": 0.5,
    "sklearn_version": sklearn.__version__,
}
joblib.dump(bundle, "model.joblib", compress=3)
b = joblib.load("model.joblib")
sorted(b)            # ['features', 'model', 'sklearn_version', 'threshold']
b["model"].predict(X[:1])
```

On load, compare `b["sklearn_version"]` with the running version. A different version may only warn, and may then give different predictions or fail later.

A serving process must never read a half-written file. Write to a temporary name, then rename. `os.replace` is atomic on one filesystem:

```python
import os
joblib.dump(bundle, "model.joblib.tmp")
os.replace("model.joblib.tmp", "model.joblib")
```

After loading, run a quick check: predict on one known row and compare with the stored answer.

## Common mistakes

- Saving only the classifier and re-creating the scaler at serving time, with different statistics.
- Loading under a different library version and ignoring the warning.
- Passing columns in a different order from training. Arrays have no names, so nothing fails and the predictions are wrong.
- Calling `fit` again after loading "to be safe", which replaces the trained model.
- Loading files from an upload or the internet.

## See also

- [scikit-learn Pipeline](#/kb/ml-sklearn-pipeline)
- [ColumnTransformer and encoders](#/kb/ml-column-transformer)
- [Atomic file writes](#/kb/prod-atomic-write)
- [Training-serving skew](#/kb/prod-train-serve-skew)
- Official docs: https://scikit-learn.org/stable/
