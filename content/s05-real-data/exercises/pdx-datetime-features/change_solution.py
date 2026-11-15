import pandas as pd


def add_time_features(orders: pd.DataFrame, weekend_days=(5, 6)) -> pd.DataFrame:
    out = orders.copy()
    ts = pd.to_datetime(out["created_at"])
    out["hour"] = ts.dt.hour
    out["weekday"] = ts.dt.weekday
    out["is_weekend"] = ts.dt.weekday.isin(list(weekend_days))
    return out
