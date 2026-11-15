import pandas as pd


def latest_per_key(df: pd.DataFrame, key: str, time_col: str, earliest: bool = False) -> pd.DataFrame:
    keep = "first" if earliest else "last"
    out = df.sort_values(time_col, kind="stable").drop_duplicates(key, keep=keep)
    return out.sort_values(key).reset_index(drop=True)
