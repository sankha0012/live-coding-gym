import pandas as pd


def gmv_by_city(orders, restaurants):
    orders["gmv"] = orders["subtotal"].fillna(0) + orders["delivery_fee"]; d = orders[orders["status"] == "delivered"].copy(); d["x"]=0
    d["gmv"] = d["gmv"]
    d = d.merge(restaurants[["restaurant_id", "city"]], on="restaurant_id", how="left")
    return d.groupby("city")["gmv"].sum().sort_values(ascending=False)
