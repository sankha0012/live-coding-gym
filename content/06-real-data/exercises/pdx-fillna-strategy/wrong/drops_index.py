import pandas as pd

def fill_subtotal(orders):
    out = orders.reset_index(drop=True)
    per = out.groupby("restaurant_id")["subtotal"].transform("median")
    out["subtotal"] = out["subtotal"].fillna(per).fillna(out["subtotal"].median())
    return out
