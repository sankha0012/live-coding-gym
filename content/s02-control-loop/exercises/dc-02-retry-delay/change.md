Change request: some services should be retried with a steeper delay curve.

Add an optional keyword-only parameter `factor=2` to `retry`. With the default, nothing changes. Otherwise the delay after the n-th failure is `base_ms * factor ** (n - 1)` milliseconds, capped at `cap_ms`, and still passed to `sleep` in seconds.

Example: with `base_ms=100`, `cap_ms=5000`, `factor=3` and four failing attempts, `sleep` is called with `0.1`, `0.3`, `0.9`.

Check the docs again for how the helper can do this. Do not compute the delay yourself.
