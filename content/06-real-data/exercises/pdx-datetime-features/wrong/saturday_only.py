import pandas as pd

def add_time_features(orders):
    out = orders.copy()
    ts = pd.to_datetime(out["created_at"])
    out["hour"] = ts.dt.hour
    out["weekday"] = ts.dt.weekday
    out["is_weekend"] = ts.dt.weekday == 5
    return out
