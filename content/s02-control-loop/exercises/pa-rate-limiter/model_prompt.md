Write a Python 3.12 class TokenBucket using only the standard library.
- Constructor: TokenBucket(capacity, refill_rate, clock=time.monotonic). capacity is the maximum number of tokens, refill_rate is tokens added per second. The bucket starts full.
- Method allow(cost=1) returns True and removes cost tokens if enough tokens are available, otherwise returns False and removes nothing.
- Refill lazily inside allow(): add (now - last) * refill_rate tokens, never above capacity, using the injected clock. Do not use threads or sleeping.
- The clock must be a parameter so tests can control time. Never call time.time() directly.
- Validate the inputs: capacity and refill_rate must be positive, cost must be positive and not above capacity. Raise ValueError otherwise. If the clock goes backwards, add no tokens and do not move the last-refill time backwards.
- Protect the state with a threading.Lock so concurrent callers are safe.
Also write pytest tests with a fake clock: the burst up to capacity, a refusal when empty, a partial refill after 0.5 seconds, no overflow above capacity after a long wait, and invalid arguments. Then explain in a few sentences why a token bucket allows bursts and how it differs from a fixed window.
