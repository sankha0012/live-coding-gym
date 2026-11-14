import pandas as pd
from solution import fix_types

IDS = ["order_id", "customer_id", "restaurant_id"]


def _raw():
    return pd.read_csv("orders.csv", dtype=str, keep_default_na=False)


def test_real_data_types():
    raw = _raw()
    got = fix_types(raw)
    assert pd.api.types.is_datetime64_any_dtype(got["created_at"])
    for c in IDS:
        assert str(got[c].dtype) == "int64", c
    assert str(got["courier_id"].dtype) == "Int64"
    assert got["courier_id"].isna().tolist() == (raw["courier_id"] == "").tolist()
    assert got["created_at"].iloc[0] == pd.Timestamp("2026-10-12 23:37:00")
    assert got["order_id"].tolist() == [int(x) for x in raw["order_id"]]


def test_coupon_empty_becomes_nan_and_codes_kept():
    raw = _raw()
    got = fix_types(raw)
    empty = raw["coupon_code"].str.strip() == ""
    assert got["coupon_code"].isna().tolist() == empty.tolist()
    assert got.loc[~empty, "coupon_code"].tolist() == raw.loc[~empty, "coupon_code"].tolist()


def test_spaces_only_coupon_and_other_columns_untouched():
    raw = _raw().head(5).copy()
    raw.loc[0, "coupon_code"] = "   "
    raw.loc[1, "coupon_code"] = "SAVE10"
    got = fix_types(raw)
    assert pd.isna(got.loc[0, "coupon_code"])
    assert got.loc[1, "coupon_code"] == "SAVE10"
    raw.loc[2, "coupon_code"] = " PROMO "
    got = fix_types(raw)
    assert got.loc[2, "coupon_code"] == " PROMO "
    assert got["subtotal"].tolist() == raw["subtotal"].tolist()
    assert got["status"].tolist() == raw["status"].tolist()


def test_input_not_modified():
    raw = _raw()
    before = raw.copy()
    fix_types(raw)
    pd.testing.assert_frame_equal(raw, before)


def test_empty_frame():
    got = fix_types(_raw().iloc[0:0])
    assert len(got) == 0
    assert pd.api.types.is_datetime64_any_dtype(got["created_at"])
