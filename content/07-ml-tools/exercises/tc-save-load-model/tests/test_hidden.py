import os
import tempfile
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from solution import save_and_load


def _fitted(seed=0):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(80, 3))
    y = (X[:, 0] - X[:, 2] > 0).astype(int)
    m = Pipeline([("s", StandardScaler()), ("m", LogisticRegression(random_state=0))])
    return m.fit(X, y), X


def test_roundtrip_identical_predictions():
    m, X = _fitted()
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "model.joblib")
        loaded = save_and_load(m, path)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0
    assert np.array_equal(loaded.predict(X), m.predict(X))
    assert np.allclose(loaded.predict_proba(X), m.predict_proba(X))


def test_returns_new_object_read_from_file():
    m, _ = _fitted()
    with tempfile.TemporaryDirectory() as d:
        loaded = save_and_load(m, Path(d) / "m.joblib")
        assert loaded is not m
        assert isinstance(loaded, Pipeline)
        assert loaded.steps[1][1] is not m.steps[1][1]


def test_overwrites_existing_file():
    m1, X = _fitted(0)
    m2, _ = _fitted(1)
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "m.joblib"
        path.write_bytes(b"not a model")
        save_and_load(m1, path)
        loaded = save_and_load(m2, path)
    assert np.allclose(loaded.predict_proba(X), m2.predict_proba(X))


def test_file_alone_is_enough():
    import joblib

    m, X = _fitted()
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "x.joblib")
        save_and_load(m, path)
        again = joblib.load(path)
    assert np.array_equal(again.predict(X), m.predict(X))


def test_uses_joblib_dump_and_load(monkeypatch):
    import joblib

    calls = []
    real_dump, real_load = joblib.dump, joblib.load
    monkeypatch.setattr(joblib, "dump", lambda *a, **k: (calls.append("dump"), real_dump(*a, **k))[1])
    monkeypatch.setattr(joblib, "load", lambda *a, **k: (calls.append("load"), real_load(*a, **k))[1])
    m, _ = _fitted()
    with tempfile.TemporaryDirectory() as d:
        save_and_load(m, os.path.join(d, "m.joblib"))
    assert calls == ["dump", "load"]
