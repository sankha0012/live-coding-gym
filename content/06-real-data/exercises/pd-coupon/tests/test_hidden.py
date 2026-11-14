import pandas as pd
from solution import coupon_effect


def test_matches_reference_on_real_data():
    orders = pd.read_csv("orders.csv")
    d = orders[orders["status"] == "delivered"]
    w = d[d["coupon_code"].notna()]["subtotal"].mean()
    wo = d[d["coupon_code"].isna()]["subtotal"].mean()
    got = coupon_effect(orders)
    assert got == (round(w, 2), round(wo, 2))


def small():
    return pd.DataFrame(
        {
            "subtotal": [10.0, 20.0, 40.0, None, 100.0, 7.0],
            "coupon_code": ["A", "B", None, None, None, "A"],
            "status": ["delivered", "delivered", "delivered", "delivered", "cancelled", "cancelled"],
        }
    )


def test_small_case_ignores_cancelled_and_null_subtotal():
    assert coupon_effect(small()) == (15.0, 40.0)


def test_returns_rounded_tuple_of_two():
    df = pd.DataFrame(
        {
            "subtotal": [10.0, 10.0, 11.0, 20.0],
            "coupon_code": ["A", "A", "A", None],
            "status": ["delivered"] * 4,
        }
    )
    got = coupon_effect(df)
    assert isinstance(got, tuple) and len(got) == 2
    assert got == (10.33, 20.0)


def test_input_not_modified():
    df = small()
    before = df.copy()
    coupon_effect(df)
    pd.testing.assert_frame_equal(df, before)
