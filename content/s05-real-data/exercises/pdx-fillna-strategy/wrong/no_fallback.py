import pandas as pd


def fill_subtotal(orders: pd.DataFrame) -> pd.DataFrame:
    out = orders.copy()
    out["subtotal"] = out["subtotal"].fillna(out.groupby("restaurant_id")["subtotal"].transform("median"))
    return out
