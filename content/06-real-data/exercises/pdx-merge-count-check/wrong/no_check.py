import pandas as pd


def merge_restaurants(orders: pd.DataFrame, restaurants: pd.DataFrame) -> pd.DataFrame:
    return orders.merge(restaurants, on="restaurant_id", how="left")
