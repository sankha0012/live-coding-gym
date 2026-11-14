import pandas as pd


def flag_orders(df):
    return df[(df["status"] == "delivered") & ((df["total"] > 100) | (df["coupon"] == None))].copy()


def count_mismatches(old, new):
    return int((old != new).sum())
