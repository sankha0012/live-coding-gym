import numpy as np
import pandas as pd
from solution import leaky_features


def build():
    rng = np.random.RandomState(7)
    n = 300
    y = pd.Series(rng.normal(size=n), name="y")
    X = pd.DataFrame(
        {
            "noise": rng.normal(size=n),
            "almost_label": y * 2 + rng.normal(scale=0.05, size=n),
            "negative_leak": -y + rng.normal(scale=0.05, size=n),
            "weak": y * 0.3 + rng.normal(size=n),
            "constant": np.ones(n),
        }
    )
    return X, y


def test_finds_positive_and_negative_leaks_sorted():
    X, y = build()
    assert leaky_features(X, y) == ["almost_label", "negative_leak"]


def test_threshold_is_strict_and_configurable():
    X, y = build()
    assert leaky_features(X, y, threshold=0.2) == ["almost_label", "negative_leak", "weak"]
    assert leaky_features(X, y, threshold=0.999999) == []


def test_constant_column_and_no_leak_and_no_columns():
    X, y = build()
    assert "constant" not in leaky_features(X, y)
    assert leaky_features(X[["noise", "weak"]], y) == []
    assert leaky_features(pd.DataFrame(index=y.index), y) == []


def test_inputs_not_modified():
    X, y = build()
    bx, by = X.copy(), y.copy()
    leaky_features(X, y)
    pd.testing.assert_frame_equal(X, bx)
    pd.testing.assert_series_equal(y, by)
