import numpy as np
import pandas as pd

from solution import count_mismatches, flag_orders


def orders():
    return pd.DataFrame(
        {
            "status": ["delivered", "delivered", "cancelled", "delivered", "delivered", "Delivered"],
            "total": [150.0, 80.0, 500.0, np.nan, 100.0, 200.0],
            "coupon": ["A10", None, None, np.nan, "B5", None],
        },
        index=[10, 11, 12, 13, 14, 15],
    )


def test_flag_orders_rows():
    assert list(flag_orders(orders()).index) == [10, 11, 13]


def test_flag_orders_keeps_columns_and_values():
    out = flag_orders(orders())
    assert list(out.columns) == ["status", "total", "coupon"]
    assert out.loc[10, "total"] == 150.0


def test_flag_orders_does_not_modify_input():
    df = orders()
    before = df.copy()
    out = flag_orders(df)
    out["total"] = 0
    pd.testing.assert_frame_equal(df, before)


def test_flag_orders_empty_result():
    df = orders().iloc[[2, 5]]
    assert len(flag_orders(df)) == 0


def test_count_mismatches_basic():
    old = pd.Series([0.1, 0.5, np.nan, np.nan, 0.9])
    new = pd.Series([0.1, 0.4, np.nan, 0.3, 0.9])
    assert count_mismatches(old, new) == 2


def test_count_mismatches_all_missing_is_equal():
    s = pd.Series([np.nan, np.nan])
    assert count_mismatches(s, s.copy()) == 0


def test_count_mismatches_returns_int():
    out = count_mismatches(pd.Series([1, 2]), pd.Series([1, 3]))
    assert out == 1 and type(out) is int
