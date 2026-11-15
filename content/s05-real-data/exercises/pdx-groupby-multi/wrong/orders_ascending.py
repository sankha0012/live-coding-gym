import pandas as pd


def city_cuisine_summary(orders, restaurants):
    m = orders.merge(restaurants, on="restaurant_id", how="inner")
    
    out = (
        m.groupby(["city", "cuisine"])
        .agg(orders=("order_id", "size"), avg_subtotal=("subtotal", "mean"))
        .reset_index()
    )
    out["avg_subtotal"] = out["avg_subtotal"].round(2)
    return out.sort_values(["orders", "city", "cuisine"], ascending=True).reset_index(drop=True)
