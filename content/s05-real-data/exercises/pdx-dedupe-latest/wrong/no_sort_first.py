import pandas as pd

def latest_per_key(df, key, time_col):
    out = df.drop_duplicates(key, keep="last")
    return out.sort_values(key).reset_index(drop=True)
