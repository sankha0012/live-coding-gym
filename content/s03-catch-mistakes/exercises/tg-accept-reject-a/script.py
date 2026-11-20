# orders.py: the script you asked the assistant to fix. This is the code BEFORE its changes.
from dataclasses import dataclass


@dataclass
class Order:
    sku: str
    qty: int
    price: float = 0.0


def parse_order(row):
    qty = int(row["qty"])
    return Order(row["sku"], qty)


def average_price(prices):
    return sum(prices) / len(prices)


def total(orders):
    t = 0
    for i in range(len(orders)):
        t += orders[i].qty * orders[i].price
    return t


def apply_discount(price, percent):
    if not percent:
        return price
    return price * (1 - percent / 100)
