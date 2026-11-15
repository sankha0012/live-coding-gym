---
title: Rate limiting with a token bucket
summary: Allow short bursts but cap the average rate by refilling tokens over time and spending one per request.
tags: [production, rate-limiting]
---
```python
class TokenBucket:
    def __init__(self, rate, capacity, clock):
        self.rate, self.capacity, self.clock = rate, capacity, clock
        self.tokens, self.last = capacity, clock()      # start full

    def allow(self, cost=1):
        now = self.clock()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now
        if self.tokens < cost:
            return False
        self.tokens -= cost
        return True
```

- Use it to protect a service or to stay under an API quota, per user or per key.
- Key rule: refill lazily from elapsed time on each call, cap at capacity, then try to spend.
- Say: "`rate` is the long-run limit, `capacity` is the burst size. No background thread is needed."

<!-- more -->

## Details

Tokens are a float. Each call first adds `elapsed * rate` tokens, never above `capacity`, then spends `cost` if enough are there.

```python
t = [0.0]
tb = TokenBucket(rate=2, capacity=3, clock=lambda: t[0])
[tb.allow() for _ in range(4)]    # [True, True, True, False]  burst of 3, then empty
t[0] = 0.5
tb.allow()                        # True   0.5 s * 2 per second = 1 new token
tb.allow()                        # False
t[0] = 100.0
round(tb.tokens + 0, 1)           # 0.0    refill happens on the next allow(), not by itself
```

A rejected call still updates `last` and keeps the refilled tokens. Nothing is lost.

For one bucket per user, keep a dict `user_id -> TokenBucket` and create the bucket on first use.

Other limiters you may be asked to compare:

- **Fixed window**: a counter per minute. Simple, but allows a double burst at the window edge.
- **Sliding window log**: a deque of timestamps. Exact, but uses memory per request.
- **Leaky bucket**: a queue drained at a fixed rate. Smooths output and adds waiting.

With threads, `allow` needs a lock, because refill and spend must be one step.

## Common mistakes

- Forgetting `min(capacity, ...)`, so an idle hour allows thousands of requests at once.
- Updating `last` only when a request is allowed, which counts the same elapsed time twice.
- Refilling whole tokens with `int(...)` and losing the fraction on every call.
- Starting empty when the task expects the first burst to pass (or the reverse). Check the spec.
- Reading `time.time()` inside the class instead of an injected monotonic clock.

## See also

- [Clocks: time.monotonic and injecting a clock or sleep](#/kb/py-time-clock-injection)
- [deque and OrderedDict](#/kb/py-collections-deque)
- [Retries with backoff](#/kb/prod-retry-backoff)
