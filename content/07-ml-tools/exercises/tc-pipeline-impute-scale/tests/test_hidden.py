import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from solution import build_model


def _data():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(60, 3))
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    X[::7, 1] = np.nan
    return X, y


def test_steps_and_order():
    m = build_model()
    assert isinstance(m, Pipeline)
    kinds = [type(s) for _, s in m.steps]
    assert kinds == [SimpleImputer, StandardScaler, LogisticRegression]
    assert m.steps[0][1].strategy == "median"
    assert m.steps[2][1].random_state == 0


def test_fits_and_predicts_with_nan():
    X, y = _data()
    m = build_model().fit(X, y)
    pred = m.predict(X)
    assert pred.shape == (60,)
    assert set(np.unique(pred)) <= {0, 1}
    assert (pred == y).mean() > 0.8


def test_median_is_learned_from_training_data():
    X = np.array([[1.0], [2.0], [100.0], [np.nan], [3.0], [4.0]])
    y = np.array([0, 0, 1, 1, 0, 1])
    m = build_model().fit(X, y)
    assert m.steps[0][1].statistics_[0] == 3.0


def test_new_object_each_call_and_unfitted():
    a, b = build_model(), build_model()
    assert a is not b
    assert a.steps[2][1] is not b.steps[2][1]
    assert not hasattr(a.steps[2][1], "coef_")


def test_predict_on_all_nan_row():
    X, y = _data()
    m = build_model().fit(X, y)
    row = np.full((1, 3), np.nan)
    assert m.predict(row).shape == (1,)


def test_fitting_one_pipeline_does_not_touch_the_next():
    X, y = _data()
    a = build_model().fit(X, y)
    b = build_model()
    assert all(sa is not sb for (_, sa), (_, sb) in zip(a.steps, b.steps))
    assert not hasattr(b.steps[0][1], "statistics_")
    assert not hasattr(b.steps[1][1], "mean_")
