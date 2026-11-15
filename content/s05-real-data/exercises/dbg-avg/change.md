Add an optional second parameter `max_minutes`, default `None`. When it is given, delivered orders whose `actual_minutes` is greater than `max_minutes` are left out of the average, because they are probably tracking errors. An order with exactly `max_minutes` stays in. If nothing is left after this filter, return `None`, as before. With the default, nothing changes.

Example: delivered orders with 20, 30 and 400 minutes and `max_minutes=60` give `25.0`; with `max_minutes=30` they give `25.0` too (30 stays in); with `max_minutes=10` they give `None`.
