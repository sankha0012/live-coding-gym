import pandas as pd


def time_split(orders: pd.DataFrame, cutoff: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    ts = pd.to_datetime(orders["created_at"])
    before = ts < pd.Timestamp(cutoff)
    return orders[before].copy(), orders[~before].copy()
