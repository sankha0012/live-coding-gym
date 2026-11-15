import pandas as pd

def time_split(orders, cutoff):
    o = orders.assign(_t=pd.to_datetime(orders["created_at"])).sort_values("_t")
    b = o["_t"] < pd.Timestamp(cutoff)
    return o[b].drop(columns="_t"), o[~b].drop(columns="_t")
