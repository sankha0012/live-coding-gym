import pandas as pd


def city_cuisine_counts(orders: pd.DataFrame, restaurants: pd.DataFrame) -> pd.DataFrame:
    d = orders[["order_id", "restaurant_id"]].merge(
        restaurants[["restaurant_id", "city", "cuisine"]], on="restaurant_id", how="left"
    )
    return d.pivot_table(index="city", columns="cuisine", values="order_id", aggfunc="count")
