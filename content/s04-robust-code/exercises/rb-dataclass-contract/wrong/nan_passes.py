import math
from dataclasses import dataclass


@dataclass
class Order:
    order_id: str
    items: int
    total: float
    status: str

    def __post_init__(self):
        problems = []
        if not isinstance(self.order_id, str) or not self.order_id:
            problems.append("order_id invalid")
        if not isinstance(self.items, int) or not 1 <= self.items <= 50:
            problems.append("items invalid")
        if not isinstance(self.total, (int, float)) or self.total < 0:
            problems.append("total invalid")
        if self.status not in ("new", "paid", "shipped"):
            problems.append("status invalid")
        if problems:
            raise ValueError("; ".join(problems))
