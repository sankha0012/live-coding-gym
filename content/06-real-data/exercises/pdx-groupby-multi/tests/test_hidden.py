import numpy as np
import pandas as pd
from solution import city_cuisine_summary

COLS = ["city", "cuisine", "orders", "avg_subtotal"]


def test_real_data_matches_reference():
    orders = pd.read_csv("orders.csv")
    restaurants = pd.read_csv("restaurants.csv")
    got = city_cuisine_summary(orders, restaurants)
    m = orders.merge(restaurants, on="restaurant_id")
    g = m.groupby(["city", "cuisine"])
    want = pd.DataFrame({"orders": g.size(), "avg_subtotal": g["subtotal"].mean().round(2)}).reset_index()
    want = want.sort_values(["orders", "city", "cuisine"], ascending=[False, True, True]).reset_index(drop=True)
    assert list(got.columns) == COLS
    pd.testing.assert_frame_equal(got, want, check_dtype=False)
    assert got["orders"].sum() == len(orders)


def _small():
    orders = pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5, 6],
        "restaurant_id": [1, 1, 2, 3, 3, 99],
        "subtotal": [10.0, np.nan, 30.0, 5.0, 6.0, 1.0],
    })
    restaurants = pd.DataFrame({
        "restaurant_id": [1, 2, 3],
        "city": ["Rio", "Rio", "Recife"],
        "cuisine": ["pizza", "sushi", "pizza"],
    })
    return orders, restaurants


def test_missing_subtotal_still_counts_and_unknown_restaurant_ignored():
    got = city_cuisine_summary(*_small())
    rows = got.values.tolist()
    assert rows == [
        ["Recife", "pizza", 2, 5.5],
        ["Rio", "pizza", 2, 10.0],
        ["Rio", "sushi", 1, 30.0],
    ]


def test_tie_order_and_index():
    got = city_cuisine_summary(*_small())
    assert got.index.tolist() == [0, 1, 2]
    assert got["city"].tolist() == ["Recife", "Rio", "Rio"]


def test_empty_orders():
    orders, restaurants = _small()
    got = city_cuisine_summary(orders.iloc[0:0], restaurants)
    assert len(got) == 0
    assert list(got.columns) == COLS


def test_cuisine_breaks_ties_within_a_city_whatever_the_row_order():
    orders = pd.DataFrame({
        "order_id": [1, 2, 3, 4, 5, 6],
        "restaurant_id": [2, 1, 3, 3, 4, 4],
        "subtotal": [10.0, 20.0, 30.0, 40.0, 50.0, 60.0],
    })
    restaurants = pd.DataFrame({
        "restaurant_id": [1, 2, 3, 4],
        "city": ["Rio", "Rio", "Recife", "Aracaju"],
        "cuisine": ["burger", "pizza", "sushi", "sushi"],
    })
    got = city_cuisine_summary(orders, restaurants)
    assert got[["city", "cuisine"]].values.tolist() == [
        ["Aracaju", "sushi"], ["Recife", "sushi"], ["Rio", "burger"], ["Rio", "pizza"],
    ]
    assert got["orders"].tolist() == [2, 2, 1, 1]
    assert got["avg_subtotal"].tolist() == [55.0, 35.0, 20.0, 10.0]
