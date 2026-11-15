import pandas as pd
from solution import time_split


def real():
    return pd.read_csv("orders.csv")


def test_matches_reference_on_real_data():
    orders = real()
    train, test = time_split(orders, "2026-10-01")
    ts = pd.to_datetime(orders["created_at"])
    assert train["order_id"].tolist() == orders.loc[ts < "2026-10-01", "order_id"].tolist()
    assert test["order_id"].tolist() == orders.loc[ts >= "2026-10-01", "order_id"].tolist()
    assert len(train) + len(test) == len(orders)
    assert list(train.columns) == list(orders.columns)


def test_no_overlap_and_train_is_older():
    orders = real()
    train, test = time_split(orders, "2026-09-15")
    assert set(train["order_id"]).isdisjoint(set(test["order_id"]))
    assert pd.to_datetime(train["created_at"]).max() < pd.to_datetime(test["created_at"]).min()


def test_row_exactly_at_cutoff_goes_to_test():
    df = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4],
            "created_at": ["2026-10-02 08:00:00", "2026-10-01 00:00:00", "2026-09-30 23:59:59", "2026-10-01 00:00:01"],
        }
    )
    train, test = time_split(df, "2026-10-01")
    assert train["order_id"].tolist() == [3]
    assert test["order_id"].tolist() == [1, 2, 4]  # original order kept
    assert test["created_at"].tolist() == ["2026-10-02 08:00:00", "2026-10-01 00:00:00", "2026-10-01 00:00:01"]  # still text


def test_empty_side_and_input_untouched():
    df = pd.DataFrame({"order_id": [1, 2], "created_at": ["2026-10-02 08:00:00", "2026-10-03 08:00:00"]})
    before = df.copy()
    train, test = time_split(df, "2026-10-01")
    assert len(train) == 0 and test["order_id"].tolist() == [1, 2]
    assert list(train.columns) == ["order_id", "created_at"]
    pd.testing.assert_frame_equal(df, before)
