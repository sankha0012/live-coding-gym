## Contract

`late_rate(orders)` takes a list of dicts and returns a `float` between 0.0 and 1.0.

Each order has `status` (`"delivered"` or `"cancelled"`), `promised_minutes` (int) and `actual_minutes` (int, or `None` when the order was cancelled).

- Only orders with `status == "delivered"` are looked at. Cancelled orders are not late and are not counted in the denominator, even if their numbers exceed the promise.
- An order is late when `actual_minutes` is strictly greater than `promised_minutes`. Arriving exactly on time is not late.
- The result is late delivered orders divided by all delivered orders.
- If there are no delivered orders (empty list, or only cancelled), the result is `0.0`, not an error.

Example: delivered 30/30, delivered 30/45 and one cancelled order give `0.5`.

## Library notes

- `len(seq)` returns an `int`; dividing two ints with `/` always gives a `float` in Python 3, but `len(x) / 0` raises `ZeroDivisionError`.
- `sum(iterable)` adds values and returns `0` for an empty iterable. Summing booleans counts the `True` values.
- `dict.get(key, default)` returns the default when the key is missing. It does not replace a key that exists with the value `None`.
- Comparing `None` with an int using `>` or `>=` raises `TypeError` in Python 3.

## Gotchas

- Rate metrics need an explicit rule for an empty denominator. A dashboard that crashes on a quiet hour or a new region is a production incident, so decide the value deliberately.
- `>` versus `>=` at the boundary changes the number silently and no exception warns you. Boundary values such as exactly on time deserve their own test.
- Filtering the population (delivered only) must happen before computing both the numerator and the denominator, otherwise the rate is diluted by orders that never had a delivery time.
