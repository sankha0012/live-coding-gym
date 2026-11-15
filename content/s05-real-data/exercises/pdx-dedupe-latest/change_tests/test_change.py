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


def test_earliest_row_wins():
    got = latest_per_key(_frame(), "id", "ts", earliest=True)
    assert got["id"].tolist() == [1, 2, 3]
    assert got["val"].tolist() == ["a1", "b0", "c1"]
    assert got.index.tolist() == [0, 1, 2]
    assert list(got.columns) == ["id", "ts", "val"]


def test_tie_keeps_the_earlier_row():
    df = pd.DataFrame({
        "id": [1, 1, 2],
        "ts": pd.to_datetime(["2026-01-01", "2026-01-01", "2026-01-02"]),
        "val": ["first", "second", "x"],
    })
    got = latest_per_key(df, "id", "ts", earliest=True)
    assert got["val"].tolist() == ["first", "x"]


def test_many_ties_keep_the_first_in_input():
    n = 200
    df = pd.DataFrame({
        "id": [i % 5 for i in range(n)],
        "ts": pd.Timestamp("2026-01-01"),
        "val": list(range(n)),
    })
    got = latest_per_key(df, "id", "ts", earliest=True)
    assert got["val"].tolist() == [0, 1, 2, 3, 4]


def test_earliest_on_real_orders_and_input_untouched():
    orders = pd.read_csv("orders.csv", parse_dates=["created_at"])
    before = orders.copy()
    got = latest_per_key(orders, "customer_id", "created_at", earliest=True)
    want = orders.groupby("customer_id")["created_at"].min()
    assert len(got) == len(want)
    assert got.set_index("customer_id")["created_at"].equals(want)
    pd.testing.assert_frame_equal(orders, before)


def test_default_still_latest():
    got = latest_per_key(_frame(), "id", "ts")
    assert got["val"].tolist() == ["a3", "b1", "c1"]
