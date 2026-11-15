import pandas as pd


def coupon_effect(orders):
    d = orders[orders["status"] == "delivered"].copy()
    d["has_coupon"] = d["coupon_code"].notna()
    means = d.groupby("has_coupon")["subtotal"].mean()
    return float(means[True]), float(means[False])
