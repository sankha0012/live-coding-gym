import pandas as pd
from solution import rolling_7d_orders


def reference(orders):
    days = pd.to_datetime(orders["created_at"]).dt.normalize()
    full = pd.date_range(days.min(), days.max(), freq="D")
    daily = [int((days == d).sum()) for d in full]
    return [sum(daily[max(0, i - 6) : i + 1]) for i in range(len(daily))], full


def test_matches_reference_on_real_data():
    orders = pd.read_csv("orders.csv")
    got = rolling_7d_orders(orders)
    want, full = reference(orders)
    assert list(got.index) == list(full)
    assert got.tolist() == want
    assert got.isna().sum() == 0
    assert got.sum() > 0


def small():
    return pd.DataFrame(
        {
            "created_at": [
                "2026-10-01 10:00:00",
                "2026-10-01 23:00:00",
                "2026-10-02 09:00:00",
                "2026-10-05 12:00:00",  # gap: 10-03 and 10-04 have no orders
                "2026-10-09 12:00:00",
            ]
        }
    )


def test_gap_days_are_counted_as_zero_and_window_is_by_days():
    got = rolling_7d_orders(small())
    assert [d.strftime("%Y-%m-%d") for d in got.index] == [f"2026-10-0{i}" for i in range(1, 10)]
    # daily: 2,1,0,0,1,0,0,0,1 -> window of 7 calendar days
    assert got.tolist() == [2, 3, 3, 3, 4, 4, 4, 2, 2]


def test_first_days_use_partial_window_and_ints():
    got = rolling_7d_orders(small())
    assert got.iloc[0] == 2
    assert all(isinstance(int(v), int) and float(v) == int(v) for v in got)


def test_empty_and_untouched():
    empty = pd.DataFrame({"created_at": []})
    assert len(rolling_7d_orders(empty)) == 0
    df = small()
    before = df.copy()
    rolling_7d_orders(df)
    pd.testing.assert_frame_equal(df, before)
