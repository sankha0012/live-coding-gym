import numpy as np
import pandas as pd
from solution import fill_subtotal


def _small():
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5, 6],
        "restaurant_id": [1, 1, 1, 2, 2, 3],
        "subtotal": [10.0, np.nan, 30.0, 100.0, 50.0, np.nan],
    })


def test_matches_reference_on_real_data():
    orders = pd.read_csv("orders.csv")
    got = fill_subtotal(orders)
    per = orders.groupby("restaurant_id")["subtotal"].transform("median")
    want = orders["subtotal"].fillna(per).fillna(orders["subtotal"].median())
    assert got["subtotal"].isna().sum() == 0
    pd.testing.assert_series_equal(got["subtotal"], want, check_names=False)
    pd.testing.assert_frame_equal(got.drop(columns="subtotal"), orders.drop(columns="subtotal"))


def test_small_frame_uses_restaurant_then_global_median():
    got = fill_subtotal(_small())
    # restaurant 1 median of 10 and 30 is 20; restaurant 3 has nothing, global median of 10,30,100,50 is 40
    assert got["subtotal"].tolist() == [10.0, 20.0, 30.0, 100.0, 50.0, 40.0]


def test_input_not_modified_and_index_kept():
    df = _small()
    df.index = [10, 11, 12, 13, 14, 15]
    before = df.copy()
    got = fill_subtotal(df)
    pd.testing.assert_frame_equal(df, before)
    assert got.index.tolist() == [10, 11, 12, 13, 14, 15]


def test_nothing_missing_and_empty():
    df = _small().dropna()
    pd.testing.assert_frame_equal(fill_subtotal(df), df)
    empty = _small().iloc[0:0]
    assert len(fill_subtotal(empty)) == 0
