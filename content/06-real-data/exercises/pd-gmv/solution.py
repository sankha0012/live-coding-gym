import pandas as pd


def gmv_by_city(orders: pd.DataFrame, restaurants: pd.DataFrame) -> pd.Series:
    d = orders[orders["status"] == "delivered"].copy()
    d["gmv"] = d["subtotal"].fillna(0) + d["delivery_fee"]
    d = d.merge(restaurants[["restaurant_id", "city"]], on="restaurant_id", how="left")
    return d.groupby("city")["gmv"].sum().sort_values(ascending=False)
