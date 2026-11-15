import pandas as pd
import numpy as np

def iqr_outliers(orders):
    s = orders["subtotal"]
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    i = q3 - q1
    m = (s < q1 - 1.5 * i) | (s > q3 + 1.5 * i)
    return [int(x) for x in orders.loc[m].sort_values("subtotal")["order_id"]]
