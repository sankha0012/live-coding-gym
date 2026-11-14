import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from solution import cv_accuracy


def _data(n=120, seed=3):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(n, 4)) * np.array([1.0, 50.0, 0.1, 5.0])
    y = (X[:, 0] + X[:, 1] / 50 + rng.normal(scale=0.8, size=n) > 0).astype(int)
    return X, y


def _reference(X, y):
    X, y = np.asarray(X), np.asarray(y)
    accs = []
    for tr, te in StratifiedKFold(n_splits=5, shuffle=True, random_state=42).split(X, y):
        m = Pipeline([("s", StandardScaler()), ("m", LogisticRegression(max_iter=1000, random_state=0))])
        m.fit(X[tr], y[tr])
        accs.append(m.score(X[te], y[te]))
    return float(np.mean(accs))


def test_matches_reference():
    X, y = _data()
    got = cv_accuracy(X, y)
    assert type(got) is float
    assert abs(got - _reference(X, y)) < 1e-12


def test_repeatable_and_inputs_untouched():
    X, y = _data()
    X0, y0 = X.copy(), y.copy()
    assert cv_accuracy(X, y) == cv_accuracy(X, y)
    assert np.array_equal(X, X0) and np.array_equal(y, y0)


def test_imbalanced_small_class():
    rng = np.random.default_rng(5)
    X = rng.normal(size=(50, 3))
    y = np.zeros(50, dtype=int)
    y[:5] = 1
    X[:5] += 2.0
    got = cv_accuracy(X, y)
    assert abs(got - _reference(X, y)) < 1e-12


def test_dataframe_and_series_input():
    X, y = _data(90, seed=8)
    df = pd.DataFrame(X, columns=list("abcd"))
    got = cv_accuracy(df, pd.Series(y))
    assert abs(got - _reference(X, y)) < 1e-12


def test_small_noisy_data_leak_sensitive():
    rng = np.random.default_rng(11)
    X = rng.normal(size=(40, 30))
    X[:, 0] *= 1000
    y = rng.integers(0, 2, size=40)
    assert abs(cv_accuracy(X, y) - _reference(X, y)) < 1e-12
