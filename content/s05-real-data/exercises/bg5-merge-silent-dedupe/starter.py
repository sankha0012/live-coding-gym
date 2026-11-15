import pandas as pd


def merge_restaurants(orders: pd.DataFrame, restaurants: pd.DataFrame) -> pd.DataFrame:
    r = restaurants.drop_duplicates("restaurant_id")
    return orders.merge(r, on="restaurant_id", how="left")
