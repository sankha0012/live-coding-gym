import pandas as pd
from solution import days_since_previous


def test_matches_reference_on_real_data():
    orders = pd.read_csv("orders.csv")
    got = days_since_previous(orders)
    t = pd.to_datetime(orders["created_at"])
    want = {}
    for _, g in pd.DataFrame({"c": orders["customer_id"], "t": t}).groupby("c"):
        g = g.sort_values("t")
        last = None
        for idx, ts in zip(g.index, g["t"]):
            want[idx] = float("nan") if last is None else (ts - last).total_seconds() / 86400
            last = ts
    want = pd.Series(want).reindex(orders.index)
    pd.testing.assert_series_equal(
        got.sort_index().astype(float).round(6), want.sort_index().round(6), check_names=False
    )


def small():
    return pd.DataFrame(
        {
            "customer_id": [1, 2, 1, 1],
            "created_at": [
                "2026-01-03 12:00:00",
                "2026-01-02 00:00:00",
                "2026-01-01 12:00:00",
                "2026-01-10 12:00:00",
            ],
        },
        index=[10, 11, 12, 13],
    )


def test_unsorted_input_and_exact_values():
    got = days_since_previous(small())
    assert sorted(got.index) == [10, 11, 12, 13]
    assert got[10] == 2.0
    assert pd.isna(got[11])
    assert pd.isna(got[12])
    assert got[13] == 7.0


def test_fractional_days():
    df = pd.DataFrame(
        {"customer_id": [5, 5], "created_at": ["2026-03-01 00:00:00", "2026-03-02 12:00:00"]}
    )
    got = days_since_previous(df)
    assert pd.isna(got[0])
    assert got[1] == 1.5


def test_single_order_customers_all_nan():
    df = pd.DataFrame(
        {"customer_id": [1, 2], "created_at": ["2026-03-01 00:00:00", "2026-03-02 00:00:00"]}
    )
    assert days_since_previous(df).isna().all()


def test_input_not_modified():
    df = small()
    before = df.copy()
    days_since_previous(df)
    pd.testing.assert_frame_equal(df, before)


def test_labels_are_kept_not_positions():
    df = pd.DataFrame(
        {"customer_id": [7, 7, 7], "created_at": ["2026-03-03", "2026-03-01", "2026-03-02"]},
        index=["c", "a", "b"],
    )
    got = days_since_previous(df)
    assert pd.isna(got["a"]) and got["b"] == 1.0 and got["c"] == 1.0
