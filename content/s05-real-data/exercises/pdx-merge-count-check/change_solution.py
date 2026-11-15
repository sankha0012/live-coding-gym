import pandas as pd


def merge_restaurants(orders: pd.DataFrame, restaurants: pd.DataFrame, require_match: bool = False) -> pd.DataFrame:
    if require_match and not orders["restaurant_id"].isin(restaurants["restaurant_id"]).all():
        raise ValueError("some orders have no matching restaurant")
    merged = orders.merge(restaurants, on="restaurant_id", how="left")
    if len(merged) != len(orders):
        raise ValueError(f"merge changed the row count: {len(orders)} -> {len(merged)}")
    return merged
