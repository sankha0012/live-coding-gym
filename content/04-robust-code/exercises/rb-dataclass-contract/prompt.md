Bad records should fail loudly at the edge of the system, and the error should list every problem, not only the first.

Write a dataclass `Order` with these fields, in this order: `order_id: str`, `items: int`, `total: float`, `status: str`. Validate in `__post_init__`. If any field is invalid, raise one `ValueError` whose message lists all problems, in field order, joined by `"; "`:

- `order_id` must be a non-empty string. Problem text: `order_id invalid`
- `items` must be an int from 1 to 50 (a bool is not valid). Problem text: `items invalid`
- `total` must be a number (int or float, not bool), not NaN, and at least 0. Problem text: `total invalid`
- `status` must be one of `"new"`, `"paid"`, `"shipped"`. Problem text: `status invalid`

A valid order is created normally. Example: an order with an empty id and `items=0` raises `ValueError("order_id invalid; items invalid")`.
