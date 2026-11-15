## Contract

`class TokenBucket(capacity, refill_per_s, clock)`, with method `allow(cost=1) -> bool`.

- `capacity` and `refill_per_s` must be greater than 0, otherwise the constructor raises `ValueError`.
- The bucket starts full. Tokens are fractional: a rate of 0.5 per second gives one whole token after two seconds, and `allow(0.5)` is valid.
- `clock()` takes no arguments and returns the current time in seconds. It is read at every `allow` call, and the constructor also reads it once to set the starting time.
- At each `allow`, the elapsed time since the previous `allow` (or the constructor) is turned into tokens, and the total is capped at `capacity`.
- If `cost` tokens are available (an exact match is enough), they are removed and the result is `True`. Otherwise the result is `False` and nothing is removed.
- A `cost` above `capacity` always returns `False`. A cost of 0 always returns `True` and takes nothing.
- If the clock goes backwards, no tokens are added or lost, and the next refill is measured from the new lower time.

## Library notes

- `min(a, b)` and `max(a, b)` return one of their arguments; `max(0, x)` is the usual way to clip a negative value.
- `time.monotonic()` returns a float in seconds that never goes backwards, unlike `time.time()`, which follows the system clock and can jump.

## Gotchas

- Keep the timestamp and the token count together; updating one without the other double-counts time.
- Do not call a real clock inside the class; accept it as an argument so tests can control time.
