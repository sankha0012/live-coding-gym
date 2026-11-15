import pandas as pd


def time_split(orders: pd.DataFrame, cutoff: str, embargo_days: int = 0) -> tuple[pd.DataFrame, pd.DataFrame]:
    ts = pd.to_datetime(orders["created_at"])
    cut = pd.Timestamp(cutoff)
    train = ts < cut - pd.Timedelta(days=embargo_days)
    test = ts >= cut
    return orders[train].copy(), orders[test].copy()
