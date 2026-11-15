import pandas as pd

def time_split(orders, cutoff):
    o = orders.copy()
    o["created_at"] = pd.to_datetime(o["created_at"])
    b = o["created_at"] < pd.Timestamp(cutoff)
    return o[b], o[~b]
