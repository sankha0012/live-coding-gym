import pandas as pd
from solution import gmv_by_city


def reference(orders, restaurants):
    d = orders[orders["status"] == "delivered"].copy()
    d["gmv"] = d["subtotal"].fillna(0) + d["delivery_fee"]
    d = d.merge(restaurants[["restaurant_id", "city"]], on="restaurant_id")
    return d.groupby("city")["gmv"].sum().sort_values(ascending=False)


def test_matches_reference_on_real_data():
    orders = pd.read_csv("orders.csv")
    restaurants = pd.read_csv("restaurants.csv")
    got = gmv_by_city(orders, restaurants)
    want = reference(orders, restaurants)
    assert list(got.index) == list(want.index)
    assert got.round(2).tolist() == want.round(2).tolist()


def small():
    orders = pd.DataFrame(
        {
            "restaurant_id": [1, 1, 2, 2, 1],
            "subtotal": [10.0, None, 20.0, 99.0, 5.0],
            "delivery_fee": [2.0, 3.0, 4.0, 1.0, 1.0],
            "status": ["delivered", "delivered", "delivered", "cancelled", "delivered"],
        }
    )
    restaurants = pd.DataFrame({"restaurant_id": [1, 2], "city": ["Rio", "Recife"]})
    return orders, restaurants


def test_small_case_missing_subtotal_and_cancelled():
    got = gmv_by_city(*small())
    assert list(got.index) == ["Recife", "Rio"]
    assert got["Rio"] == 21.0  # 12 + 3 + 6
    assert got["Recife"] == 24.0


def test_sorted_largest_first():
    got = gmv_by_city(pd.read_csv("orders.csv"), pd.read_csv("restaurants.csv"))
    assert got.is_monotonic_decreasing


def test_inputs_not_modified():
    orders, restaurants = small()
    before = orders.copy()
    gmv_by_city(orders, restaurants)
    pd.testing.assert_frame_equal(orders, before)
