import pandas as pd
from solution import gmv_by_city


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


def test_cancelled_also_counted():
    got = gmv_by_city(*small(), statuses=("delivered", "cancelled"))
    assert list(got.index) == ["Recife", "Rio"]
    assert got["Recife"] == 124.0  # 24 + 100
    assert got["Rio"] == 21.0


def test_only_cancelled_and_empty_selection():
    got = gmv_by_city(*small(), statuses=("cancelled",))
    assert got.to_dict() == {"Recife": 100.0}
    assert len(gmv_by_city(*small(), statuses=("refunded",))) == 0


def test_real_data_all_statuses_sorted():
    orders = pd.read_csv("orders.csv")
    restaurants = pd.read_csv("restaurants.csv")
    got = gmv_by_city(orders, restaurants, statuses=tuple(orders["status"].unique()))
    d = orders.copy()
    d["gmv"] = d["subtotal"].fillna(0) + d["delivery_fee"]
    d = d.merge(restaurants[["restaurant_id", "city"]], on="restaurant_id")
    want = d.groupby("city")["gmv"].sum().sort_values(ascending=False)
    assert list(got.index) == list(want.index)
    assert got.round(2).tolist() == want.round(2).tolist()
    assert got.is_monotonic_decreasing


def test_default_and_input_untouched():
    orders, restaurants = small()
    before = orders.copy()
    got = gmv_by_city(orders, restaurants, statuses=("delivered", "cancelled"))
    pd.testing.assert_frame_equal(orders, before)
    assert gmv_by_city(orders, restaurants).to_dict() == {"Recife": 24.0, "Rio": 21.0}
