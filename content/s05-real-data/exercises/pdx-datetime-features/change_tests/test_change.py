import pandas as pd
from solution import add_time_features


def _frame():
    # 2026-10-12 Monday, 10-16 Friday, 10-17 Saturday, 10-18 Sunday
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4],
        "created_at": ["2026-10-12 23:37:00", "2026-10-16 08:59:59", "2026-10-17 00:15:00", "2026-10-18 12:00:00"],
    })


def test_friday_saturday_weekend():
    got = add_time_features(_frame(), weekend_days=(4, 5))
    assert got["is_weekend"].tolist() == [False, True, True, False]
    assert got["weekday"].tolist() == [0, 4, 5, 6]
    assert got["hour"].tolist() == [23, 8, 0, 12]


def test_single_day_and_list_and_empty_set():
    assert add_time_features(_frame(), weekend_days=[0])["is_weekend"].tolist() == [True, False, False, False]
    assert add_time_features(_frame(), weekend_days={6})["is_weekend"].tolist() == [False, False, False, True]
    assert add_time_features(_frame(), weekend_days=())["is_weekend"].tolist() == [False] * 4


def test_dtype_empty_frame_and_real_data():
    got = add_time_features(_frame(), weekend_days=(4,))
    assert got["is_weekend"].dtype == bool
    empty = add_time_features(_frame().iloc[0:0], weekend_days=(4, 5))
    assert len(empty) == 0 and empty["is_weekend"].dtype == bool
    orders = pd.read_csv("orders.csv")
    ts = pd.to_datetime(orders["created_at"])
    got = add_time_features(orders, weekend_days=(4, 5))
    assert got["is_weekend"].tolist() == ts.dt.dayofweek.isin([4, 5]).tolist()
    assert got["created_at"].tolist() == orders["created_at"].tolist()


def test_default_still_saturday_sunday_and_input_untouched():
    df = _frame()
    before = df.copy()
    got = add_time_features(df, weekend_days=(4, 5))
    pd.testing.assert_frame_equal(df, before)
    assert add_time_features(df)["is_weekend"].tolist() == [False, False, True, True]
