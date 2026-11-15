import pandas as pd


def iqr_outliers(orders: pd.DataFrame, k: float = 1.5) -> list[int]:
    s = orders["subtotal"]
    if s.dropna().empty:
        return []
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    mask = (s < q1 - k * iqr) | (s > q3 + k * iqr)
    return sorted(int(i) for i in orders.loc[mask, "order_id"])
