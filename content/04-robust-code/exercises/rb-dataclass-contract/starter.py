import math
from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    items: int
    total: float
    status: str

    def __post_init__(self):
        pass
