import pandas as pd
import pytest
from solution import merge_restaurants

R = pd.DataFrame({"restaurant_id": [1, 2], "city": ["Rio", "Recife"]})


def test_unmatched_order_raises_when_required():
    orders = pd.DataFrame({"order_id": [1, 2, 3], "restaurant_id": [1, 2, 99]})
    with pytest.raises(ValueError):
        merge_restaurants(orders, R, require_match=True)


def test_unmatched_order_kept_by_default():
    orders = pd.DataFrame({"order_id": [1, 2, 3], "restaurant_id": [1, 2, 99]})
    assert len(merge_restaurants(orders, R)) == 3
    assert len(merge_restaurants(orders, R, require_match=False)) == 3


def test_all_matched_is_fine_when_required():
    orders = pd.DataFrame({"order_id": [1, 2, 3], "restaurant_id": [2, 1, 2]})
    got = merge_restaurants(orders, R, require_match=True)
    assert got["city"].tolist() == ["Recife", "Rio", "Recife"]


def test_unused_restaurants_are_fine_and_empty_orders_never_raise():
    orders = pd.DataFrame({"order_id": [1], "restaurant_id": [1]})
    many = pd.DataFrame({"restaurant_id": [1, 2, 3], "city": ["a", "b", "c"]})
    assert len(merge_restaurants(orders, many, require_match=True)) == 1
    assert len(merge_restaurants(orders.iloc[0:0], R, require_match=True)) == 0


def test_real_data_and_inputs_untouched():
    orders = pd.read_csv("orders.csv")
    restaurants = pd.read_csv("restaurants.csv")
    o_before, r_before = orders.copy(), restaurants.copy()
    ok = orders["restaurant_id"].isin(restaurants["restaurant_id"]).all()
    if ok:
        assert len(merge_restaurants(orders, restaurants, require_match=True)) == len(orders)
    bad = pd.concat([orders, orders.iloc[[0]].assign(restaurant_id=10**6)], ignore_index=True)
    with pytest.raises(ValueError):
        merge_restaurants(bad, restaurants, require_match=True)
    pd.testing.assert_frame_equal(orders, o_before)
    pd.testing.assert_frame_equal(restaurants, r_before)
