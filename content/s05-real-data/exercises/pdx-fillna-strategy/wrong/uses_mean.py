import pandas as pd

def fill_subtotal(orders):
    out = orders.copy()
    per = out.groupby("restaurant_id")["subtotal"].transform("mean")
    out["subtotal"] = out["subtotal"].fillna(per).fillna(out["subtotal"].median())
    return out
