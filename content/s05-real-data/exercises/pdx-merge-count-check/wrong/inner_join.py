import pandas as pd


def merge_restaurants(orders: pd.DataFrame, restaurants: pd.DataFrame) -> pd.DataFrame:
    merged = orders.merge(restaurants, on="restaurant_id", how="inner")
    if len(merged) != len(orders):
        raise ValueError("row count changed")
    return merged
