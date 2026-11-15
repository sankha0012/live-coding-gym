import pandas as pd
from solution import latest_per_key


def _frame():
    return pd.DataFrame({
        "id": [2, 1, 1, 3, 2, 1],
        "ts": pd.to_datetime([
            "2026-01-01 09:00", "2026-01-01 10:00", "2026-01-01 12:00",
            "2026-01-01 08:00", "2026-01-01 07:00", "2026-01-01 11:00",
        ]),
        "val": ["b1", "a1", "a3", "c1", "b0", "a2"],
    })


def test_latest_row_wins_not_the_last_in_file():
    got = latest_per_key(_frame(), "id", "ts")
    assert got["id"].tolist() == [1, 2, 3]
    assert got["val"].tolist() == ["a3", "b1", "c1"]
    assert got.index.tolist() == [0, 1, 2]
    assert list(got.columns) == ["id", "ts", "val"]


def test_tie_keeps_the_later_row():
    df = pd.DataFrame({
        "id": [1, 1, 2],
        "ts": pd.to_datetime(["2026-01-01", "2026-01-01", "2026-01-02"]),
        "val": ["first", "second", "x"],
    })
    got = latest_per_key(df, "id", "ts")
    assert got["val"].tolist() == ["second", "x"]


def test_many_ties_keep_the_last_in_input():
    n = 200
    df = pd.DataFrame({
        "id": [i % 5 for i in range(n)],
        "ts": pd.Timestamp("2026-01-01"),
        "val": list(range(n)),
    })
    got = latest_per_key(df, "id", "ts")
    assert got["val"].tolist() == [195, 196, 197, 198, 199]


def test_input_not_modified():
    df = _frame()
    before = df.copy()
    latest_per_key(df, "id", "ts")
    pd.testing.assert_frame_equal(df, before)


def test_empty_frame():
    got = latest_per_key(_frame().iloc[0:0], "id", "ts")
    assert len(got) == 0
    assert list(got.columns) == ["id", "ts", "val"]


def test_orders_one_row_per_customer():
    orders = pd.read_csv("orders.csv", parse_dates=["created_at"])
    got = latest_per_key(orders, "customer_id", "created_at")
    assert len(got) == orders["customer_id"].nunique()
    want = orders.groupby("customer_id")["created_at"].max()
    assert got.set_index("customer_id")["created_at"].equals(want)


def test_whole_row_kept_even_when_latest_has_missing_values():
    df = pd.DataFrame({
        "id": [1, 1, 2],
        "ts": pd.to_datetime(["2026-01-01 09:00", "2026-01-01 10:00", "2026-01-01 08:00"]),
        "val": ["old", None, "x"],
        "n": [5.0, None, 7.0],
    })
    got = latest_per_key(df, "id", "ts")
    assert got["ts"].tolist() == pd.to_datetime(["2026-01-01 10:00", "2026-01-01 08:00"]).tolist()
    assert got["val"].isna().tolist() == [True, False]
    assert got["n"].isna().tolist() == [True, False]
