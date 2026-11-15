import pandas as pd
from solution import iqr_outliers


def test_matches_reference_on_real_data():
    orders = pd.read_csv("orders.csv")
    s = orders["subtotal"].dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    i = q3 - q1
    want = sorted(orders.loc[(orders["subtotal"] < q1 - 1.5 * i) | (orders["subtotal"] > q3 + 1.5 * i), "order_id"].tolist())
    got = iqr_outliers(orders)
    assert got == want
    assert len(got) > 0
    assert all(type(x) is int for x in got)


def small(values):
    return pd.DataFrame({"order_id": range(100, 100 + len(values)), "subtotal": values})


def test_low_and_high_outliers_sorted():
    # Q1=10, Q3=14, IQR=4, fences 4 and 20
    df = small([30.0, 10.0, 12.0, 14.0, 11.0, 13.0, 10.0, 14.0, 1.0, 12.0])
    got = iqr_outliers(df)
    assert got == [100, 108]


def test_missing_values_ignored_and_never_flagged():
    df = small([10.0, None, 11.0, 12.0, 13.0, 14.0, None, 200.0])
    got = iqr_outliers(df)
    assert got == [107]


def test_nothing_flagged_and_empty():
    assert iqr_outliers(small([10.0, 11.0, 12.0, 13.0, 14.0])) == []
    assert iqr_outliers(pd.DataFrame({"order_id": [], "subtotal": []})) == []


def test_value_on_the_fence_is_not_outlier():
    # values 0,0,0,0,4,4,4,4 -> Q1=0, Q3=4, IQR=4, upper fence 10
    df = small([0.0, 0.0, 0.0, 0.0, 4.0, 4.0, 4.0, 10.0])
    assert iqr_outliers(df) == []


def test_input_untouched():
    df = small([30.0, 10.0, 12.0, 14.0, 1.0])
    before = df.copy()
    iqr_outliers(df)
    pd.testing.assert_frame_equal(df, before)


def test_missing_values_do_not_shift_quartiles():
    # without the NaNs: Q1=11.25, Q3=13.75, upper fence 17.5, so 25 is flagged
    df = small([10.0, 11.0, 12.0, 13.0, 14.0, 25.0] + [None] * 6)
    assert iqr_outliers(df) == [105]


def test_quartiles_use_linear_interpolation():
    # linear: Q1=4, Q3=9.25, fences -3.875 and 17.125 -> only 24 is flagged
    assert iqr_outliers(small([3.0, 4.0, 4.0, 5.0, 5.0, 8.0, 17.0, 24.0])) == [107]
    # linear: Q1=11.5, Q3=18, fences 1.75 and 27.75 -> only 1.0 is flagged
    assert iqr_outliers(small([1.0, 7.0, 13.0, 13.0, 16.0, 16.0, 24.0, 27.0])) == [100]


def test_ids_sorted_when_rows_are_not():
    df = pd.DataFrame({"order_id": [9, 4, 7, 1, 6, 3, 8, 2], "subtotal": [50.0, 10.0, 11.0, 12.0, 13.0, 14.0, 11.5, 1.0]})
    assert iqr_outliers(df) == [2, 9]
