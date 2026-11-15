Change: cap the wait. Add an optional last parameter `max_delay=None` to `call_with_retry`, so the signature is `call_with_retry(fn, retries, sleep, base_delay=1.0, max_delay=None)`.

When `max_delay` is not `None`, no single sleep may be longer than `max_delay`: sleep for `min(base_delay * 2 ** (k - 1), max_delay)`. With `max_delay=None` the behaviour is exactly as before. For example, with `retries=4`, `base_delay=1.0` and `max_delay=3.0`, the sleeps are `[1.0, 2.0, 3.0, 3.0]`.

Do this by hand in your own passing solution. It should take two or three lines.
