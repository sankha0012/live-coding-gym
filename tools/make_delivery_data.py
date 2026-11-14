"""Generate the shared food-delivery dataset used by SQL and pandas exercises.

Run: uv run python tools/make_delivery_data.py   (writes content/_shared/)
"""
import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

CITIES = ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba"]
CITY_WEIGHTS = [0.4, 0.25, 0.2, 0.15]
CUISINES = ["japanese", "pizza", "brazilian", "burger", "healthy", "arabic"]
VEHICLES = ["bike", "motorbike", "car"]
COUPONS = [None, "BEMVINDO10", "FRETEGRATIS", "PIZZA20"]
COUPON_WEIGHTS = [0.7, 0.1, 0.15, 0.05]

SCHEMA = """CREATE TABLE restaurants (restaurant_id INTEGER PRIMARY KEY, name TEXT, city TEXT, cuisine TEXT);
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT, signup_date TEXT);
CREATE TABLE couriers (courier_id INTEGER PRIMARY KEY, name TEXT, vehicle TEXT);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, restaurant_id INTEGER, courier_id INTEGER, created_at TEXT, subtotal REAL, delivery_fee REAL, coupon_code TEXT, status TEXT, promised_minutes INTEGER, actual_minutes REAL);
"""

TABLE_COLUMNS = {
    "restaurants": ["restaurant_id", "name", "city", "cuisine"],
    "customers": ["customer_id", "name", "city", "signup_date"],
    "couriers": ["courier_id", "name", "vehicle"],
    "orders": ["order_id", "customer_id", "restaurant_id", "courier_id", "created_at", "subtotal",
               "delivery_fee", "coupon_code", "status", "promised_minutes", "actual_minutes"],
}


def build_rows():
    rnd = random.Random(2026)
    pick = lambda items, weights=None: rnd.choices(items, weights)[0]
    restaurants = [(i, f"Rest {i:02d}", pick(CITIES, CITY_WEIGHTS), CUISINES[(i * 7) % 6]) for i in range(1, 25)]
    start = datetime(2026, 8, 1)
    customers = [(i, f"Customer {i:03d}", pick(CITIES, CITY_WEIGHTS),
                  (start - timedelta(days=rnd.randrange(1, 400))).strftime("%Y-%m-%d")) for i in range(1, 401)]
    couriers = [(i, f"Courier {i:02d}", pick(VEHICLES)) for i in range(1, 81)]
    orders = []
    for i in range(1500):
        created = start + timedelta(minutes=rnd.randrange(92 * 24 * 60))
        rid = 1 + int(rnd.random() * rnd.random() * 24 + rnd.random() * 6) % 24
        delivered = rnd.random() >= 0.08
        promised = pick([30, 40, 50])
        slow = 1.25 if rid % 5 == 0 else 1.0
        noise = math.exp((rnd.random() + rnd.random() + rnd.random() - 1.5) * 0.35)
        actual = round(promised * slow * noise, 1) if delivered else None
        subtotal = round(20 + rnd.random() * 60 + rnd.random() * rnd.random() * 120, 2)
        if rnd.random() < 0.01:
            subtotal = None
        customer = 1 + int(rnd.random() * rnd.random() * 400)
        courier = 1 + rnd.randrange(80) if delivered else None
        orders.append((100001 + i, customer, rid, courier, created.strftime("%Y-%m-%d %H:%M:%S"), subtotal,
                       pick([0, 4.99, 6.99, 8.99]), pick(COUPONS, COUPON_WEIGHTS),
                       "delivered" if delivered else "cancelled", promised, actual))
    return {"restaurants": restaurants, "customers": customers, "couriers": couriers, "orders": orders}


def sql_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, str):
        return "'" + v.replace("'", "''") + "'"
    return repr(v)


def generate(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tables = build_rows()
    lines = [SCHEMA.rstrip()]
    for name, rows in tables.items():
        cols = ", ".join(TABLE_COLUMNS[name])
        lines += [f"INSERT INTO {name} ({cols}) VALUES ({', '.join(sql_value(v) for v in row)});" for row in rows]
        with (out_dir / f"{name}.csv").open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(TABLE_COLUMNS[name])
            writer.writerows([["" if v is None else v for v in row] for row in rows])
    (out_dir / "delivery.sql").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent / "content" / "_shared")
