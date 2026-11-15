Change request: some clients send a request and a retry with the very same timestamp, so the limiter must be able to count a request made exactly at `now` as well.

Add an optional keyword-only parameter `include_now=False` to `is_rate_limited`. With the default, nothing changes. With `include_now=True`, an earlier request whose time is exactly `now` counts towards the limit, while the window still starts at `now - window` (inclusive) and nothing after `now` is counted.

Example: `is_rate_limited([95, 100], 100, 10, 2)` is `False`, but `is_rate_limited([95, 100], 100, 10, 2, include_now=True)` is `True`.

Check the docs again for how to make the helper include its upper bound. Do not just add 1 to `now`.
