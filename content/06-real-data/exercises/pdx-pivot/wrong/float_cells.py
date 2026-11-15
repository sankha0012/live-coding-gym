import pandas as pd

def city_cuisine_counts(orders, restaurants):
    d = orders.merge(restaurants, on="restaurant_id")
    return d.groupby(["city", "cuisine"]).size().unstack().fillna(0).astype(float)
