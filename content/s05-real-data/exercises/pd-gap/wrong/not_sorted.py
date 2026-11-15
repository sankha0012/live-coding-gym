import pandas as pd


def days_since_previous(orders: pd.DataFrame) -> pd.Series:
    o = orders.copy()
    o["created_at"] = pd.to_datetime(o["created_at"])
    prev = o.groupby("customer_id")["created_at"].shift(1)
    return (o["created_at"] - prev).dt.total_seconds() / 86400
