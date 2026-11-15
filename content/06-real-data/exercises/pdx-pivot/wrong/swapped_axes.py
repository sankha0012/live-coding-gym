import pandas as pd

def city_cuisine_counts(orders, restaurants):
    d = orders.merge(restaurants, on="restaurant_id")
    return pd.crosstab(d["cuisine"], d["city"])
