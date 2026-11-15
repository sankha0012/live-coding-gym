import pandas as pd

def merge_restaurants(orders, restaurants):
    merged = orders.merge(restaurants, on="restaurant_id", how="left", sort=True)
    if len(merged) != len(orders):
        raise ValueError("rows")
    return merged
