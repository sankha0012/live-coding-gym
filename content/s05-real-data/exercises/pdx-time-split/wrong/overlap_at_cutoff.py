import pandas as pd


def time_split(orders: pd.DataFrame, cutoff: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    ts = pd.to_datetime(orders["created_at"])
    c = pd.Timestamp(cutoff)
    return orders[ts <= c].copy(), orders[ts >= c].copy()
