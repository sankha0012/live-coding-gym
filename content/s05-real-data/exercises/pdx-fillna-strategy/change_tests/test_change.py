import numpy as np
import pandas as pd
from solution import fill_subtotal


def _small():
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5, 6],
        "restaurant_id": [1, 1, 1, 2, 2, 3],
        "subtotal": [10.0, np.nan, 30.0, 100.0, 50.0, np.nan],
    })


def test_flag_marks_original_missing_rows():
    got = fill_subtotal(_small(), add_flag=True)
    assert got["subtotal_was_missing"].tolist() == [False, True, False, False, False, True]
    assert got["subtotal_was_missing"].dtype == bool
    assert got["subtotal"].tolist() == [10.0, 20.0, 30.0, 100.0, 50.0, 40.0]
    assert list(got.columns) == ["order_id", "restaurant_id", "subtotal", "subtotal_was_missing"]


def test_flag_keeps_index_and_input_untouched():
    df = _small()
    df.index = [10, 11, 12, 13, 14, 15]
    before = df.copy()
    got = fill_subtotal(df, add_flag=True)
    assert got.index.tolist() == [10, 11, 12, 13, 14, 15]
    assert got["subtotal_was_missing"].sum() == 2
    pd.testing.assert_frame_equal(df, before)


def test_default_adds_no_column():
    assert "subtotal_was_missing" not in fill_subtotal(_small()).columns
    assert "subtotal_was_missing" not in fill_subtotal(_small(), add_flag=False).columns


def test_flag_on_real_data_and_empty():
    orders = pd.read_csv("orders.csv")
    got = fill_subtotal(orders, add_flag=True)
    assert got["subtotal_was_missing"].tolist() == orders["subtotal"].isna().tolist()
    assert got["subtotal"].isna().sum() == 0
    empty = fill_subtotal(_small().iloc[0:0], add_flag=True)
    assert len(empty) == 0 and "subtotal_was_missing" in empty.columns
