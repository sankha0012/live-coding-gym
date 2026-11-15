import pandas as pd

def time_split(orders, cutoff):
    orders["created_at"] = pd.to_datetime(orders["created_at"])
    b = orders["created_at"] < pd.Timestamp(cutoff)
    return orders[b], orders[~b]
