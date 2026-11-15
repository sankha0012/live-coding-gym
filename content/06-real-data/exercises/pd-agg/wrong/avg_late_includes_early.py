import pandas as pd


def city_dashboard(orders, restaurants):
    d = orders[orders["status"] == "delivered"].copy()
    d = d.merge(restaurants[["restaurant_id", "city"]], on="restaurant_id", how="left")
    d["late"] = d["actual_minutes"] > d["promised_minutes"]
    d["minutes_late"] = (d["actual_minutes"] - d["promised_minutes"])
    out = d.groupby("city").agg(
        orders=("order_id", "count"),
        late_rate=("late", "mean"),
        avg_late=("minutes_late", lambda s: s[s != 0].mean()),
    )
    return out
