import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from solution import build_preprocessor


def _frame():
    return pd.DataFrame({
        "age": [20.0, 30.0, 40.0, 50.0],
        "fee": [1.0, 2.0, 3.0, 10.0],
        "city": ["a", "b", "a", "c"],
        "id": [101, 102, 103, 104],
    })


def test_types_and_options():
    ct = build_preprocessor(["age", "fee"], ["city"])
    assert isinstance(ct, ColumnTransformer)
    kinds = [type(t) for _, t, _ in ct.transformers]
    assert kinds == [StandardScaler, OneHotEncoder]
    enc = ct.transformers[1][1]
    assert enc.handle_unknown == "ignore"
    assert enc.sparse_output is False


def test_output_layout_and_scaling():
    df = _frame()
    out = build_preprocessor(["age", "fee"], ["city"]).fit_transform(df)
    out = np.asarray(out)
    assert out.shape == (4, 2 + 3)
    assert np.allclose(out[:, :2].mean(axis=0), 0.0)
    assert np.allclose(out[:, :2].std(axis=0), 1.0)
    assert out[:, 2:].tolist() == [[1, 0, 0], [0, 1, 0], [1, 0, 0], [0, 0, 1]]


def test_unknown_category_gives_zeros():
    ct = build_preprocessor(["age"], ["city"])
    ct.fit(_frame())
    new = pd.DataFrame({"age": [35.0], "city": ["zzz"], "id": [1]})
    out = np.asarray(ct.transform(new))
    assert out.shape == (1, 4)
    assert out[0, 1:].tolist() == [0, 0, 0]


def test_only_categorical_and_only_numeric():
    df = _frame()
    only_cat = np.asarray(build_preprocessor([], ["city"]).fit_transform(df))
    assert only_cat.shape == (4, 3)
    only_num = np.asarray(build_preprocessor(["age"], []).fit_transform(df))
    assert only_num.shape == (4, 1)


def test_new_object_each_call_and_input_untouched():
    df = _frame()
    before = df.copy()
    a, b = build_preprocessor(["age"], ["city"]), build_preprocessor(["age"], ["city"])
    assert a is not b
    a.fit_transform(df)
    pd.testing.assert_frame_equal(df, before)


def test_returned_unfitted():
    from sklearn.exceptions import NotFittedError
    from sklearn.utils.validation import check_is_fitted

    ct = build_preprocessor(["age"], ["city"])
    try:
        check_is_fitted(ct)
    except NotFittedError:
        return
    raise AssertionError("preprocessor must not be fitted")
