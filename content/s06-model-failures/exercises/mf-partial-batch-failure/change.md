Add an optional third parameter `fill=None`: `score_batch(rows, score_fn, fill=None)`. A bad row now holds `fill` in `"scores"` instead of `None`. `"errors"` is unchanged. With `fill` not given, nothing changes.

For example, with a `score_fn` that raises `ValueError("price is negative")` for negative prices, `score_batch([{"price": 1}, {"price": -5}], score_fn, fill=0.0)` returns `{"scores": [2, 0.0], "errors": [{"index": 1, "reason": "ValueError: price is negative"}]}` when good rows score `price * 2`.
