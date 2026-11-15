Read this listing. It runs on Python 3.12.

```python
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def make_data(n=400, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 5))
    X[:, 0] *= 50
    X[:, 0] += 200
    y = (X[:, 1] + 0.01 * (X[:, 0] - 200) + rng.normal(0, 1, n) > 0).astype(int)
    return X, y


def train_and_score(X, y, seed=0):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.25, random_state=seed, stratify=y
    )
    model = LogisticRegression(max_iter=500)
    model.fit(X_train, y_train)
    scores = model.predict_proba(X_test)[:, 1]
    return roc_auc_score(y_test, scores)


if __name__ == "__main__":
    X, y = make_data()
    print(round(train_and_score(X, y), 4))
```

Explain this code as you would to the interviewer after finishing it: what it does, how, complexity, one risk.
