import pandas as pd


def coupon_effect(orders):
    d = orders[orders["status"] != "cancelled"].copy()
    d["has_coupon"] = d["coupon_code"].notna()
    means = d.groupby("has_coupon")["subtotal"].mean()
    return round(float(means[True]), 2), round(float(means[False]), 2)
