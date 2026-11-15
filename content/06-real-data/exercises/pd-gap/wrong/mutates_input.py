import pandas as pd


def days_since_previous(orders):
    o = orders
    o["created_at"] = pd.to_datetime(o["created_at"])
    o = o.sort_values(["customer_id", "created_at"])
    prev = o.groupby("customer_id")["created_at"].shift(1)
    gap = (o["created_at"] - prev).dt.total_seconds() / 86400
    return gap.reindex(orders.index)
