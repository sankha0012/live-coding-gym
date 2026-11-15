import pandas as pd

def city_cuisine_counts(orders, restaurants):
    d = orders.merge(restaurants, on="restaurant_id", how="right")
    d["n"] = d["order_id"].notna().astype(int)
    return d.pivot_table(index="city", columns="cuisine", values="n", aggfunc="sum", fill_value=0)
