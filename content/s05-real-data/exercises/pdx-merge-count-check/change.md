Add an optional third parameter `require_match`, default `False`. When it is `True`, also raise `ValueError` if any order has a `restaurant_id` that does not exist in `restaurants`. Orders must be checked, not restaurants: a restaurant nobody ordered from is fine. With the default, orders without a restaurant are still kept with NaN, as before. An empty `orders` frame never raises.

Example: orders with restaurant ids `1, 2, 99` and restaurants `1, 2` raise `ValueError` with `require_match=True`, and return 3 rows with the default.
