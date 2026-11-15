Write the class `TokenBucket(capacity, refill_per_s, clock)` to protect an API from too many calls.

- The bucket holds up to `capacity` tokens and starts full. It gains `refill_per_s` tokens per second, but never goes above `capacity`.
- `allow(cost=1)` returns `True` and removes `cost` tokens if at least `cost` tokens are available, otherwise it returns `False` and removes nothing.
- `clock` is a function returning the current time in seconds. Read it at each call to `allow`, and refill by the time passed since the previous call to `allow` (or since the constructor).
- If the clock goes backwards, add no tokens and do not lose any. The next refill is measured from the new, lower time.
- `capacity` and `refill_per_s` must be greater than 0, else `ValueError`.
- A `cost` greater than `capacity` can never succeed: return `False`.

An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
