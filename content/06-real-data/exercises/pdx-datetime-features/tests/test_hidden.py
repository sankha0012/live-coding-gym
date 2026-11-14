import pandas as pd
from solution import add_time_features


def _frame():
    # 2026-10-12 is a Monday, 2026-10-17 a Saturday, 2026-10-18 a Sunday
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4],
        "created_at": ["2026-10-12 23:37:00", "2026-10-17 00:15:00", "2026-10-18 12:00:00", "2026-10-16 08:59:59"],
    })


def test_known_values():
    got = add_time_features(_frame())
    assert got["hour"].tolist() == [23, 0, 12, 8]
    assert got["weekday"].tolist() == [0, 5, 6, 4]
    assert got["is_weekend"].tolist() == [False, True, True, False]


def test_real_data_matches_reference():
    orders = pd.read_csv("orders.csv")
    got = add_time_features(orders)
    ts = pd.to_datetime(orders["created_at"])
    assert got["hour"].tolist() == ts.dt.hour.tolist()
    assert got["weekday"].tolist() == ts.dt.dayofweek.tolist()
    assert got["is_weekend"].tolist() == (ts.dt.dayofweek >= 5).tolist()
    assert got["created_at"].tolist() == orders["created_at"].tolist()
    assert len(got) == len(orders)


def test_types_and_input_not_modified():
    df = _frame()
    before = df.copy()
    got = add_time_features(df)
    pd.testing.assert_frame_equal(df, before)
    assert pd.api.types.is_integer_dtype(got["hour"])
    assert pd.api.types.is_integer_dtype(got["weekday"])
    assert got["is_weekend"].dtype == bool


def test_empty_frame():
    got = add_time_features(_frame().iloc[0:0])
    assert len(got) == 0
    assert {"hour", "weekday", "is_weekend"} <= set(got.columns)
