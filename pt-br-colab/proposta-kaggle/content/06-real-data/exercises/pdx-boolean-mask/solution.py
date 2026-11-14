import pandas as pd


def flag_orders(df):
    delivered = df["status"] == "delivered"
    big_or_no_coupon = (df["total"] > 100) | df["coupon"].isna()
    return df[delivered & big_or_no_coupon].copy()


def count_mismatches(old, new):
    both_missing = old.isna() & new.isna()
    return int(((old != new) & ~both_missing).sum())
