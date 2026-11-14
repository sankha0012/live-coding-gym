import pandas as pd
from solution import city_dashboard


def reference(orders, restaurants):
    d = orders[orders["status"] == "delivered"].merge(
        restaurants[["restaurant_id", "city"]], on="restaurant_id"
    )
    rows = {}
    for city, g in d.groupby("city"):
        diff = g["actual_minutes"] - g["promised_minutes"]
        late = diff[diff > 0]
        rows[city] = (len(g), len(late) / len(g), late.mean() if len(late) else float("nan"))
    return pd.DataFrame(rows, index=["orders", "late_rate", "avg_late"]).T


def check(got, want):
    got = got.sort_index()
    want = want.sort_index()
    assert list(got.columns) == ["orders", "late_rate", "avg_late"]
    assert list(got.index) == list(want.index)
    assert got["orders"].tolist() == want["orders"].tolist()
    pd.testing.assert_series_equal(
        got["late_rate"].round(4), want["late_rate"].round(4), check_names=False, check_dtype=False
    )
    pd.testing.assert_series_equal(
        got["avg_late"].round(4), want["avg_late"].round(4), check_names=False, check_dtype=False
    )


def test_matches_reference_on_real_data():
    orders = pd.read_csv("orders.csv")
    restaurants = pd.read_csv("restaurants.csv")
    check(city_dashboard(orders, restaurants), reference(orders, restaurants))


def small():
    orders = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4, 5],
            "restaurant_id": [1, 1, 1, 2, 2],
            "status": ["delivered", "delivered", "cancelled", "delivered", "delivered"],
            "promised_minutes": [30, 30, 30, 30, 40],
            "actual_minutes": [40.0, 20.0, None, 25.0, 40.0],
        }
    )
    restaurants = pd.DataFrame({"restaurant_id": [1, 2], "city": ["Rio", "Recife"]})
    return orders, restaurants


def test_small_case_exact_values():
    got = city_dashboard(*small()).sort_index()
    assert got.loc["Rio", "orders"] == 2
    assert got.loc["Rio", "late_rate"] == 0.5
    assert got.loc["Rio", "avg_late"] == 10.0
    assert got.loc["Recife", "orders"] == 2
    assert got.loc["Recife", "late_rate"] == 0.0


def test_city_without_late_orders_has_nan_avg_late():
    got = city_dashboard(*small())
    assert pd.isna(got.loc["Recife", "avg_late"])


def test_inputs_not_modified():
    orders, restaurants = small()
    before = orders.copy()
    city_dashboard(orders, restaurants)
    pd.testing.assert_frame_equal(orders, before)
