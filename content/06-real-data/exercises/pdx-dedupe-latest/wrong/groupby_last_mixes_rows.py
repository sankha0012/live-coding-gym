import pandas as pd

def latest_per_key(df, key, time_col):
    return df.sort_values(time_col, kind="stable").groupby(key, as_index=False).last()
