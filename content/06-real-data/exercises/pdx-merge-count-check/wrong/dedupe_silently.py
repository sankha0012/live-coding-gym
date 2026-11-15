import pandas as pd

def merge_restaurants(orders, restaurants):
    r = restaurants.drop_duplicates("restaurant_id")
    return orders.merge(r, on="restaurant_id", how="left")
