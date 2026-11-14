import pandas as pd


def latest_per_key(df: pd.DataFrame, key: str, time_col: str) -> pd.DataFrame:
    out = df.sort_values(time_col, kind="stable").drop_duplicates(key, keep="last")
    return out.sort_values(key).reset_index(drop=True)
