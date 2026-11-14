import math
from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    items: int
    total: float
    status: str

    def __post_init__(self):
        if not isinstance(self.order_id, str) or not self.order_id:
            raise ValueError("order_id invalid")
        if isinstance(self.items, bool) or not isinstance(self.items, int) or not 1 <= self.items <= 50:
            raise ValueError("items invalid")
        t = self.total
        if isinstance(t, bool) or not isinstance(t, (int, float)) or math.isnan(t) or t < 0:
            raise ValueError("total invalid")
        if self.status not in ("new", "paid", "shipped"):
            raise ValueError("status invalid")
