---
title: ColumnTransformer and encoders
summary: Apply different preprocessing to different columns, such as scaling numbers and one-hot encoding categories.
tags: [machine learning, scikit-learn, encoding]
---
```python
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

X = pd.DataFrame({"city": ["SP", "RJ", "SP", "BH", "RJ", "SP"],
                  "subtotal": [50.0, 80.0, 70.0, 120.0, 65.0, 90.0],
                  "minutes": [30, 45, 38, 60, 41, 35]})
pre = ColumnTransformer([
    ("num", StandardScaler(), ["subtotal", "minutes"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"]),
])
pre.fit_transform(X).shape          # (6, 5)  2 scaled columns + 3 city columns
pre.get_feature_names_out()         # num__subtotal, num__minutes, cat__city_BH, cat__city_RJ, cat__city_SP
```

- Each entry is `(name, transformer, list_of_columns)`.
- Columns you do not list are dropped unless you pass `remainder="passthrough"`.
- `handle_unknown="ignore"` encodes a category unseen in training as all zeros instead of raising.

<!-- more -->

## Details

`OneHotEncoder` makes one 0/1 column per category. The categories are learned in `fit` and sorted, so the output columns are stable.

A transformer can itself be a pipeline, for example impute then scale. The whole thing then goes in front of a model:

```python
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

X.loc[2, "subtotal"] = np.nan
y = [0, 1, 0, 1, 1, 0]
num = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())])
pre = ColumnTransformer([
    ("num", num, ["subtotal", "minutes"]),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["city"]),
])
model = Pipeline([("pre", pre), ("clf", LogisticRegression())]).fit(X, y)

new = pd.DataFrame({"city": ["XX"], "subtotal": [70.0], "minutes": [40]})
pre.transform(new).round(2)         # [[-0.5, -0.16, 0., 0., 0.]]  unknown city -> all zeros
model.predict(new)                  # array([0])
```

The median, the scaling statistics and the category list all come from the training rows. New data is only transformed.

Other encoder options:

- `OneHotEncoder(sparse_output=False)` returns a dense array. The default output is a sparse matrix.
- `OneHotEncoder(drop="first")` drops one column per feature. Useful for linear models without regularisation.
- `OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)` gives one integer per category. Good for tree models, misleading for linear ones because it invents an order.

Select columns by type with `make_column_selector(dtype_include="number")` instead of typing the names.

Nested parameter names chain with double underscores: `pre__num__impute__strategy`.

## Common mistakes

- Leaving out `handle_unknown="ignore"`. The first new category in production raises `ValueError: Found unknown categories`.
- Passing a single column as a string, `"city"`, to an encoder. Encoders need 2-D input, so use a list: `["city"]`.
- Forgetting that unlisted columns disappear. Check the output shape.
- Using `pd.get_dummies` separately on train and test. The two frames can end up with different columns.
- Fitting the transformer on all data before the split.

## See also

- [scikit-learn Pipeline](#/kb/ml-sklearn-pipeline)
- [Train/test splits and data leakage](#/kb/ml-train-test-split-leakage)
- [Missing values: isna, fillna, dropna](#/kb/pd-missing-values)
- Official docs: https://scikit-learn.org/stable/
