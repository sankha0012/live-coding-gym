# Rate limits and backpressure

## What it is

A rate limit caps how many requests a caller may make in a period. A token bucket is the usual algorithm: it holds up to a fixed number of tokens, refills at a steady rate, and each request spends one. Backpressure is the other side of the same idea: when a system cannot keep up, it pushes back on the producer by rejecting, slowing or shedding work instead of accepting everything and collapsing. See [token bucket](#/kb/prod-rate-limiter-token-bucket).

## How it breaks in production

Without a limit, one noisy client or one retry storm uses all the capacity, and every other client sees timeouts. The worst case is an unbounded queue: memory grows, latency climbs because each item waits behind thousands of others, and eventually the process dies and queued work is lost. Rate limiters break in their own ways. A fixed window lets a client send a full quota at the end of one window and again at the start of the next. A limiter that rejects with no hint makes clients retry immediately and make things worse, so a rejection should say when to come back (HTTP 429 with a retry delay).

## The defence in code

```python
from collections import deque

class TokenBucket:
    def __init__(self, capacity: float, rate: float, clock):
        self.capacity, self.rate, self.clock = capacity, rate, clock
        self.tokens, self.last = capacity, clock()

    def allow(self) -> bool:
        now = self.clock()
        self.tokens = min(self.capacity, self.tokens + max(0.0, now - self.last) * self.rate)
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False

class BoundedQueue:
    def __init__(self, limit: int):
        self.items, self.limit = deque(), limit

    def offer(self, item) -> bool:
        if len(self.items) >= self.limit:
            return False                    # shed load: the caller gets a 429 or 503
        self.items.append(item)
        return True

t = [0.0]
bucket = TokenBucket(capacity=2, rate=1, clock=lambda: t[0])
print([bucket.allow() for _ in range(3)])   # [True, True, False]
t[0] = 1.0
print(bucket.allow())                       # True: one token refilled

q = BoundedQueue(2)
print([q.offer(i) for i in range(3)])       # [True, True, False]
```

The bucket allows a burst up to its capacity, then a steady rate, and ignores a clock that steps back. The queue's hard limit turns overload into a fast rejection.

## What to say in the interview

"I protect a service in two places. A token bucket limits each caller to a steady rate with a small allowed burst, and the rejection tells them when to retry. Inside the service I use a bounded queue, so under overload I reject early rather than let latency and memory grow without limit. Clients should retry with backoff and jitter, otherwise they turn a brief overload into a longer one."
