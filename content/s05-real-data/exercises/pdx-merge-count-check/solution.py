import pandas as pd


def merge_restaurants(orders: pd.DataFrame, restaurants: pd.DataFrame) -> pd.DataFrame:
    merged = orders.merge(restaurants, on="restaurant_id", how="left")
    if len(merged) != len(orders):
        raise ValueError(f"merge changed the row count: {len(orders)} -> {len(merged)}")
    return merged
