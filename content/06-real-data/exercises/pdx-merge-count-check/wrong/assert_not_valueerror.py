import pandas as pd

def merge_restaurants(orders, restaurants):
    merged = orders.merge(restaurants, on="restaurant_id", how="left")
    assert len(merged) == len(orders)
    return merged
