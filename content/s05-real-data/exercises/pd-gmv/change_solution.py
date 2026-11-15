import pandas as pd


def gmv_by_city(orders: pd.DataFrame, restaurants: pd.DataFrame, statuses: tuple = ("delivered",)) -> pd.Series:
    d = orders[orders["status"].isin(statuses)].copy()
    d["gmv"] = d["subtotal"].fillna(0) + d["delivery_fee"]
    d = d.merge(restaurants[["restaurant_id", "city"]], on="restaurant_id", how="left")
    return d.groupby("city")["gmv"].sum().sort_values(ascending=False)
