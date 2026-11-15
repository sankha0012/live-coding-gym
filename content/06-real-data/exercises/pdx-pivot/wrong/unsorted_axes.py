import pandas as pd

def city_cuisine_counts(orders, restaurants):
    d = orders.merge(restaurants, on="restaurant_id")
    return d.groupby(["city", "cuisine"], sort=False).size().unstack(fill_value=0)
