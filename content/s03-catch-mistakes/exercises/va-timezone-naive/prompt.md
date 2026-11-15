An AI assistant wrote this. The tests fail. Find the bug and fix it with the smallest safe change.

`is_expired(expires_at, now)` returns `True` when `now` is at or after `expires_at`. Both are `datetime` objects. A naive datetime (no tzinfo) is treated as UTC. An aware datetime is converted to UTC, so `2024-01-01 12:00-03:00` is the same instant as `2024-01-01 15:00 UTC`. Comparing a naive and an aware value must not raise. The inputs are not modified.
