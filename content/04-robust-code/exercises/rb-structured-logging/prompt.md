Log lines that machines can search are dicts, not strings. Write `make_record(level, event, fields, clock)`.

- `level` must be one of `"debug"`, `"info"`, `"warning"`, `"error"`. Anything else raises `ValueError`.
- `event` must be a non-empty string, else `ValueError`.
- `fields` is a dict of extra data, or `None` (same as empty).
- `clock` is a function returning a number. Call it exactly once and store the value under `"ts"`.
- Return a new flat dict: `"level"`, `"event"`, `"ts"` and then every key of `fields`.
- The names `level`, `event` and `ts` are reserved. If `fields` uses any of them, raise `ValueError` naming the key, and never overwrite the real value.
- Do not change the `fields` dict you were given.

Example: `make_record("info", "order_paid", {"order_id": 7}, lambda: 100.0)` returns `{"level": "info", "event": "order_paid", "ts": 100.0, "order_id": 7}`.
