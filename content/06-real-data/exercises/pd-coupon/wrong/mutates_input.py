import pandas as pd


def coupon_effect(orders):
    orders["has_coupon"] = orders["coupon_code"].notna()
    d = orders[orders["status"] == "delivered"]
    means = d.groupby("has_coupon")["subtotal"].mean()
    return round(float(means[True]), 2), round(float(means[False]), 2)
