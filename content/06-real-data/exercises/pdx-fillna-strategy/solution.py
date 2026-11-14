import pandas as pd


def fill_subtotal(orders: pd.DataFrame) -> pd.DataFrame:
    out = orders.copy()
    per_restaurant = out.groupby("restaurant_id")["subtotal"].transform("median")
    out["subtotal"] = out["subtotal"].fillna(per_restaurant).fillna(out["subtotal"].median())
    return out
