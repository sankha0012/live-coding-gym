import pandas as pd


def city_cuisine_summary(orders: pd.DataFrame, restaurants: pd.DataFrame) -> pd.DataFrame:
    m = orders.merge(restaurants, on="restaurant_id", how="inner")
    out = (
        m.groupby(["city", "cuisine"])
        .agg(orders=("order_id", "size"), avg_subtotal=("subtotal", "mean"))
        .reset_index()
    )
    out["avg_subtotal"] = out["avg_subtotal"].round(2)
    return out
