import csv
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from make_delivery_data import generate  # noqa: E402


def test_dataset_shape_and_determinism(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    generate(a)
    generate(b)
    for name in ("delivery.sql", "orders.csv", "restaurants.csv", "customers.csv", "couriers.csv"):
        assert (a / name).read_bytes() == (b / name).read_bytes()
    db = sqlite3.connect(":memory:")
    db.executescript((a / "delivery.sql").read_text())
    count = lambda q: db.execute(q).fetchone()[0]
    assert count("SELECT COUNT(*) FROM restaurants") == 24
    assert count("SELECT COUNT(*) FROM customers") == 400
    assert count("SELECT COUNT(*) FROM couriers") == 80
    assert count("SELECT COUNT(*) FROM orders") == 1500
    cancelled = count("SELECT COUNT(*) FROM orders WHERE status = 'cancelled'")
    assert 60 <= cancelled <= 180
    assert count("SELECT COUNT(*) FROM orders WHERE status = 'cancelled' AND (courier_id IS NOT NULL OR actual_minutes IS NOT NULL)") == 0
    assert 1 <= count("SELECT COUNT(*) FROM orders WHERE subtotal IS NULL") <= 40
    assert count("SELECT MIN(created_at) >= '2026-08-01' FROM orders") == 1
    slow = db.execute("SELECT AVG(actual_minutes / promised_minutes) FROM orders o WHERE status = 'delivered' AND restaurant_id % 5 = 0").fetchone()[0]
    fast = db.execute("SELECT AVG(actual_minutes / promised_minutes) FROM orders o WHERE status = 'delivered' AND restaurant_id % 5 != 0").fetchone()[0]
    assert slow > fast * 1.1
    rows = list(csv.DictReader((a / "orders.csv").open()))
    assert len(rows) == 1500 and rows[0].keys() >= {"order_id", "subtotal", "status"}
