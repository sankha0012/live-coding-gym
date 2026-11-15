import pandas as pd

def merge_restaurants(orders, restaurants):
    if restaurants["restaurant_id"].duplicated().any():
        raise ValueError("dup")
    return orders.merge(restaurants, on="restaurant_id", how="left")
