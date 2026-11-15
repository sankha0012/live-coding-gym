import pandas as pd


def rolling_7d_orders(orders: pd.DataFrame) -> pd.Series:
    if orders.empty:
        return pd.Series([], dtype="int64", index=pd.DatetimeIndex([]))
    days = pd.to_datetime(orders["created_at"]).dt.normalize()
    daily = days.value_counts().sort_index()
    return daily.rolling(7, min_periods=1).sum().astype("int64")
