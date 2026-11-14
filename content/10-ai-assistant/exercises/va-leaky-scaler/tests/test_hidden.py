import numpy as np
from sklearn.model_selection import train_test_split
from solution import prepare


def _data():
    rng = np.random.default_rng(0)
    X = np.column_stack([
        rng.normal(10, 2, 40),
        rng.normal(-5, 20, 40) + np.arange(40),
    ])
    y = (X[:, 0] > 10).astype(int)
    return X, y


def test_scaler_fit_on_train_only():
    X, y = _data()
    X_tr, X_te, _, _ = train_test_split(X, y, test_size=0.25, random_state=3)
    *_, scaler = prepare(X, y, 3)
    assert np.allclose(scaler.mean_, X_tr.mean(axis=0))
    assert np.allclose(scaler.scale_, X_tr.std(axis=0))
    assert not np.allclose(scaler.mean_, X.mean(axis=0))


def test_train_standardised_and_test_uses_train_stats():
    X, y = _data()
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=3)
    X_tr_s, X_te_s, a, b, _ = prepare(X, y, 3)
    assert np.array_equal(a, y_tr) and np.array_equal(b, y_te)
    assert np.allclose(X_tr_s.mean(axis=0), 0, atol=1e-9)
    want = (X_te - X_tr.mean(axis=0)) / X_tr.std(axis=0)
    assert np.allclose(X_te_s, want)


def test_split_sizes_and_labels():
    X, y = _data()
    X_tr_s, X_te_s, y_tr, y_te, _ = prepare(X, y, 1)
    assert len(X_tr_s) == 30 and len(X_te_s) == 10
    assert len(y_tr) == 30 and len(y_te) == 10


def test_deterministic_and_seed_matters():
    X, y = _data()
    a = prepare(X, y, 7)
    b = prepare(X, y, 7)
    c = prepare(X, y, 8)
    assert np.array_equal(a[0], b[0]) and np.array_equal(a[2], b[2])
    assert not np.array_equal(a[2], c[2]) or not np.array_equal(a[0], c[0])
