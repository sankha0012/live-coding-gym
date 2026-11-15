import pandas as pd

def latest_per_key(df, key, time_col):
    out = df.sort_values(time_col, kind="stable").drop_duplicates(key, keep="last")
    return out.reset_index(drop=True)
