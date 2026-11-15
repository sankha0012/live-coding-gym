import pandas as pd

def rolling_7d_orders(orders):
    if orders.empty:
        return pd.Series([], dtype="int64", index=pd.DatetimeIndex([]))
    days = pd.to_datetime(orders["created_at"]).dt.normalize()
    daily = days.value_counts().sort_index()
    full = pd.date_range(daily.index.min(), daily.index.max(), freq="D")
    daily = daily.reindex(full, fill_value=0)
    return (days.value_counts().sort_index().rolling("7D").sum()).astype("int64")
