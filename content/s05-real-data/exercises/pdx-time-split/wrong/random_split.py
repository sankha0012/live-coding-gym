import pandas as pd


def time_split(orders: pd.DataFrame, cutoff: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    shuffled = orders.sample(frac=1.0, random_state=0)
    n = int(len(orders) * 0.8)
    return shuffled.iloc[:n], shuffled.iloc[n:]
