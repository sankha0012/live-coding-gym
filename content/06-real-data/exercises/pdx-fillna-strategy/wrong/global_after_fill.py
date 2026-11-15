import pandas as pd

def fill_subtotal(orders):
    out = orders.copy()
    per = out.groupby("restaurant_id")["subtotal"].transform("median")
    out["subtotal"] = out["subtotal"].fillna(per)
    out["subtotal"] = out["subtotal"].fillna(out["subtotal"].median())
    return out
