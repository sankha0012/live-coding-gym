import pandas as pd
import pytest
from solution import merge_restaurants


def test_real_data_matches_reference():
    orders = pd.read_csv("orders.csv")
    restaurants = pd.read_csv("restaurants.csv")
    got = merge_restaurants(orders, restaurants)
    want = orders.merge(restaurants, on="restaurant_id", how="left")
    assert len(got) == len(orders)
    pd.testing.assert_frame_equal(got.reset_index(drop=True), want)


def test_duplicate_restaurant_key_raises():
    orders = pd.read_csv("orders.csv")
    restaurants = pd.read_csv("restaurants.csv")
    dup = pd.concat([restaurants, restaurants.iloc[[0]]], ignore_index=True)
    with pytest.raises(ValueError):
        merge_restaurants(orders, dup)


def test_order_without_restaurant_is_kept():
    orders = pd.DataFrame({"order_id": [1, 2, 3], "restaurant_id": [1, 99, 2]})
    restaurants = pd.DataFrame({"restaurant_id": [1, 2], "city": ["Rio", "Recife"]})
    got = merge_restaurants(orders, restaurants)
    assert got["order_id"].tolist() == [1, 2, 3]
    assert got["city"].tolist()[0] == "Rio"
    assert pd.isna(got["city"].tolist()[1])
    assert got["city"].tolist()[2] == "Recife"


def test_inputs_not_modified_and_empty_orders():
    orders = pd.DataFrame({"order_id": [1, 2], "restaurant_id": [1, 2]})
    restaurants = pd.DataFrame({"restaurant_id": [1, 2], "city": ["Rio", "Recife"]})
    o_before, r_before = orders.copy(), restaurants.copy()
    merge_restaurants(orders, restaurants)
    pd.testing.assert_frame_equal(orders, o_before)
    pd.testing.assert_frame_equal(restaurants, r_before)
    assert len(merge_restaurants(orders.iloc[0:0], restaurants)) == 0


def test_duplicate_key_nobody_uses_is_not_an_error():
    orders = pd.DataFrame({"order_id": [1, 2], "restaurant_id": [1, 2]})
    restaurants = pd.DataFrame({"restaurant_id": [1, 2, 5, 5], "city": ["Rio", "Recife", "A", "B"]})
    got = merge_restaurants(orders, restaurants)
    assert got["order_id"].tolist() == [1, 2]
    assert got["city"].tolist() == ["Rio", "Recife"]


def test_unsorted_inputs_not_modified_even_on_the_error_path():
    orders = pd.DataFrame({"order_id": [3, 1, 2], "restaurant_id": [2, 1, 2]}, index=[7, 8, 9])
    restaurants = pd.DataFrame({"restaurant_id": [2, 1, 2], "city": ["Recife", "Rio", "Olinda"]})
    o_before, r_before = orders.copy(), restaurants.copy()
    with pytest.raises(ValueError):
        merge_restaurants(orders, restaurants)
    pd.testing.assert_frame_equal(orders, o_before)
    pd.testing.assert_frame_equal(restaurants, r_before)
    good = restaurants.iloc[:2].iloc[::-1]
    g_before = good.copy()
    got = merge_restaurants(orders, good)
    assert got["order_id"].tolist() == [3, 1, 2]
    pd.testing.assert_frame_equal(orders, o_before)
    pd.testing.assert_frame_equal(good, g_before)
