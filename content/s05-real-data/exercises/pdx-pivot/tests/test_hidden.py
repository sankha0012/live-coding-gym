import pandas as pd
from solution import city_cuisine_counts


def check(got, want):
    assert list(got.index) == list(want.index)
    assert list(got.columns) == list(want.columns)
    assert got.isna().sum().sum() == 0
    assert got.to_numpy().tolist() == want.to_numpy().tolist()


def test_matches_reference_on_real_data():
    orders = pd.read_csv("orders.csv")
    restaurants = pd.read_csv("restaurants.csv")
    got = city_cuisine_counts(orders, restaurants)
    d = orders.merge(restaurants, on="restaurant_id")
    want = pd.crosstab(d["city"], d["cuisine"])
    check(got, want)
    assert got.to_numpy().sum() == len(orders)


def small():
    orders = pd.DataFrame({"order_id": [1, 2, 3, 4, 5], "restaurant_id": [1, 1, 2, 3, 3]})
    restaurants = pd.DataFrame(
        {
            "restaurant_id": [1, 2, 3, 4, 5],
            "city": ["Rio", "Rio", "Recife", "Recife", "Salvador"],
            "cuisine": ["pizza", "japanese", "pizza", "japanese", "bbq"],
        }
    )
    return orders, restaurants


def test_small_case_zero_fill_and_order():
    got = city_cuisine_counts(*small())
    assert list(got.index) == ["Recife", "Rio"]
    assert list(got.columns) == ["japanese", "pizza"]
    assert got.to_numpy().tolist() == [[0, 2], [1, 2]]


def test_unused_restaurant_and_integer_cells():
    got = city_cuisine_counts(*small())
    assert got.shape == (2, 2)
    assert all(str(t).startswith("int") for t in got.dtypes)


def test_inputs_not_modified():
    orders, restaurants = small()
    b1, b2 = orders.copy(), restaurants.copy()
    city_cuisine_counts(orders, restaurants)
    pd.testing.assert_frame_equal(orders, b1)
    pd.testing.assert_frame_equal(restaurants, b2)
