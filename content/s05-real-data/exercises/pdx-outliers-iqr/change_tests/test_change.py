import pandas as pd
from solution import iqr_outliers


def small(values):
    return pd.DataFrame({"order_id": range(100, 100 + len(values)), "subtotal": values})


def test_wider_fence_flags_less():
    # Q1=11.25, Q3=13.75, IQR=2.5: upper fence is 17.5 (k=1.5), 23.75 (k=4), 26.25 (k=5)
    df = small([10.0, 11.0, 12.0, 13.0, 14.0, 25.0])
    assert iqr_outliers(df, k=1.5) == [105]
    assert iqr_outliers(df, k=4) == [105]
    assert iqr_outliers(df, k=5) == []


def test_narrower_fence_flags_more():
    # Q1=11.25, Q3=13.75, IQR=2.5, k=0.5: fences 10 and 15 -> 14 is inside, 10 is on the fence
    df = small([10.0, 11.0, 12.0, 13.0, 14.0, 25.0])
    assert iqr_outliers(df, k=0.5) == [105]
    # k=0: fences are Q1=11.25 and Q3=13.75 -> everything outside the box is flagged
    assert iqr_outliers(df, k=0) == [100, 101, 104, 105]


def test_value_on_the_new_fence_is_not_outlier():
    # Q1=0, Q3=4, IQR=4; k=2 -> upper fence 12, lower fence -8
    df = small([0.0, 0.0, 0.0, 0.0, 4.0, 4.0, 4.0, 12.0])
    assert iqr_outliers(df, k=2) == []
    assert iqr_outliers(df, k=1.9) == [107]


def test_k_with_missing_values_and_real_data():
    df = small([10.0, None, 11.0, 12.0, 13.0, 14.0, None, 25.0])
    assert iqr_outliers(df, k=5) == []
    assert iqr_outliers(df, k=1.5) == [107]
    orders = pd.read_csv("orders.csv")
    s = orders["subtotal"].dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    i = q3 - q1
    want = sorted(orders.loc[(orders["subtotal"] < q1 - 3 * i) | (orders["subtotal"] > q3 + 3 * i), "order_id"].tolist())
    assert iqr_outliers(orders, k=3) == want


def test_default_k_still_1_5():
    df = small([10.0, 11.0, 12.0, 13.0, 14.0, 25.0])
    assert iqr_outliers(df) == iqr_outliers(df, k=1.5) == [105]
