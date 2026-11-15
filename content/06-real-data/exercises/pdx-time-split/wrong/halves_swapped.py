import pandas as pd

def time_split(orders, cutoff):
    ts = pd.to_datetime(orders["created_at"])
    b = ts < pd.Timestamp(cutoff)
    return orders[~b].copy(), orders[b].copy()
