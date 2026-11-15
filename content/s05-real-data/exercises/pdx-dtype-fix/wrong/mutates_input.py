import pandas as pd

ID_COLS = ["order_id", "customer_id", "restaurant_id"]


def fix_types(raw: pd.DataFrame) -> pd.DataFrame:
    raw["created_at"] = pd.to_datetime(raw["created_at"])
    raw["coupon_code"] = raw["coupon_code"].where(raw["coupon_code"].str.strip() != "")
    raw[ID_COLS] = raw[ID_COLS].astype("int64")
    raw["courier_id"] = pd.to_numeric(raw["courier_id"].replace("", None)).astype("Int64")
    return raw
