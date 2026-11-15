Write `average_delivery_minutes(orders)`. `orders` is a list of dicts with `status` and `actual_minutes` (a number, or `None` when unknown). It returns the average of `actual_minutes` over the orders with status `"delivered"` and a known time, as a float. It returns `None` if there are no such orders.

An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
