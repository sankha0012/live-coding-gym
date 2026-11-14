import pandas as pd


def iqr_outliers(orders: pd.DataFrame) -> list[int]:
    s = orders["subtotal"]
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    mask = s > q3 + 1.5 * (q3 - q1)
    return sorted(int(i) for i in orders.loc[mask, "order_id"])
