import pandas as pd
ID_COLS = ["order_id", "customer_id", "restaurant_id"]

def fix_types(raw):
    out = raw.copy()
    out["created_at"] = pd.to_datetime(out["created_at"])
    out["coupon_code"] = out["coupon_code"].str.strip().where(out["coupon_code"].str.strip() != "")
    out[ID_COLS] = out[ID_COLS].astype("int64")
    out["courier_id"] = pd.to_numeric(out["courier_id"].replace("", None)).astype("Int64")
    
    return out
