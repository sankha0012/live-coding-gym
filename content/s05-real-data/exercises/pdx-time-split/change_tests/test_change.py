import pandas as pd
from solution import time_split


def test_gap_rows_are_in_neither_frame():
    df = pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5, 6],
        "created_at": ["2026-09-28 23:59:59", "2026-09-29 00:00:00", "2026-09-30 12:00:00",
                       "2026-10-01 00:00:00", "2026-10-05 08:00:00", "2026-09-01 10:00:00"],
    })
    before = df.copy()
    train, test = time_split(df, "2026-10-01", embargo_days=2)
    assert train["order_id"].tolist() == [1, 6]
    assert test["order_id"].tolist() == [4, 5]
    assert train["created_at"].tolist() == ["2026-09-28 23:59:59", "2026-09-01 10:00:00"]
    pd.testing.assert_frame_equal(df, before)


def test_default_has_no_gap():
    df = pd.DataFrame({"order_id": [1, 2], "created_at": ["2026-09-30 23:00:00", "2026-10-01 00:00:00"]})
    train, test = time_split(df, "2026-10-01")
    assert train["order_id"].tolist() == [1]
    assert test["order_id"].tolist() == [2]
    train, test = time_split(df, "2026-10-01", embargo_days=0)
    assert train["order_id"].tolist() == [1]


def test_real_data_embargo():
    orders = pd.read_csv("orders.csv")
    train, test = time_split(orders, "2026-10-01", embargo_days=3)
    ts = pd.to_datetime(orders["created_at"])
    assert train["order_id"].tolist() == orders.loc[ts < "2026-09-28", "order_id"].tolist()
    assert test["order_id"].tolist() == orders.loc[ts >= "2026-10-01", "order_id"].tolist()
    assert len(train) + len(test) < len(orders)
    assert list(train.columns) == list(orders.columns)


def test_embargo_can_empty_train():
    df = pd.DataFrame({"order_id": [1], "created_at": ["2026-09-30 08:00:00"]})
    train, test = time_split(df, "2026-10-01", embargo_days=5)
    assert len(train) == 0 and len(test) == 0
    assert list(train.columns) == ["order_id", "created_at"]
