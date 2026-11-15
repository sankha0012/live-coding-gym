import pandas as pd

def fill_subtotal(orders):
    out = orders.copy()
    m = out.groupby("restaurant_id")["subtotal"].median()
    out["subtotal"] = out["subtotal"].fillna(out["restaurant_id"].map(m)).fillna(m.median())
    return out
