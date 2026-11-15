import pandas as pd
from solution import fix_types


def _raw():
    return pd.read_csv("orders.csv", dtype=str, keep_default_na=False).head(6).copy()


def test_listed_tokens_become_nan_after_strip():
    raw = _raw()
    raw["coupon_code"] = ["N/A", " NULL ", "SAVE10", "", "null", "  "]
    got = fix_types(raw, na_values=("N/A", "NULL"))
    assert got["coupon_code"].isna().tolist() == [True, True, False, True, False, True]
    assert got.loc[2, "coupon_code"] == "SAVE10"
    assert got.loc[4, "coupon_code"] == "null"


def test_real_data_with_extra_tokens():
    raw = pd.read_csv("orders.csv", dtype=str, keep_default_na=False)
    codes = raw["coupon_code"].str.strip()
    token = codes[codes != ""].iloc[0]
    got = fix_types(raw, na_values=(token,))
    want = (codes == "") | (codes == token)
    assert got["coupon_code"].isna().tolist() == want.tolist()
    assert got["courier_id"].isna().tolist() == (raw["courier_id"] == "").tolist()


def test_default_and_empty_tuple_unchanged():
    raw = _raw()
    raw["coupon_code"] = ["N/A", "x", "", " ", "y", "z"]
    a = fix_types(raw)
    b = fix_types(raw, na_values=())
    assert a["coupon_code"].isna().tolist() == [False, False, True, True, False, False]
    pd.testing.assert_frame_equal(a, b)


def test_input_not_modified_with_tokens():
    raw = _raw()
    raw["coupon_code"] = ["N/A"] * 6
    before = raw.copy()
    fix_types(raw, na_values=("N/A",))
    pd.testing.assert_frame_equal(raw, before)
