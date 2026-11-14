import pandas as pd


def iqr_outliers(orders: pd.DataFrame) -> list[int]:
    s = orders["subtotal"]
    mask = (s - s.mean()).abs() > 3 * s.std()
    return sorted(int(i) for i in orders.loc[mask, "order_id"])
