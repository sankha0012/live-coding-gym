# Caching with expiry

## What it is

A cache keeps the result of an expensive call, such as a feature lookup or a model score, so the next identical request is answered from memory. A time-to-live (TTL) gives each entry an expiry time, after which it is treated as missing and recomputed. TTL is the simplest answer to "how stale may this be", and a size limit with least-recently-used eviction bounds memory. See [TTL cache](#/kb/prod-ttl-cache), [clock injection](#/kb/py-time-clock-injection) and [LRU cache](#/kb/algo-lru-cache).

## How it breaks in production

Stale data is the main failure: a cached price or a customer feature outlives the real value, and the model scores on yesterday's world. A hard expiry causes a second problem: when a popular key expires, many requests miss at once and all hit the backend together, a stampede. Caching the wrong thing hurts too. If you cache an error or a `None`, a one-second outage becomes a one-hour outage. Code bugs are common: using the wall clock, which can jump, instead of a monotonic clock, comparing with `<` when an entry should expire at exactly the TTL, and building a cache with no size limit that eventually eats the memory.

## The defence in code

```python
import time

class TTLCache:
    def __init__(self, ttl: float, max_size: int = 1000, clock=time.monotonic):
        self.ttl, self.max_size, self.clock = ttl, max_size, clock
        self.data = {}                      # key -> (expires_at, value); dict keeps insertion order

    def get(self, key, load):
        now = self.clock()
        hit = self.data.get(key)
        if hit and now < hit[0]:
            return hit[1]
        value = load(key)                   # an exception here is not cached
        self.data.pop(key, None)
        self.data[key] = (now + self.ttl, value)
        while len(self.data) > self.max_size:
            del self.data[next(iter(self.data))]    # drop the oldest insert
        return value

t = [0.0]
cache = TTLCache(ttl=10, clock=lambda: t[0])
calls = []
load = lambda k: calls.append(k) or k.upper()
cache.get("a", load); cache.get("a", load)
t[0] = 10.0                                  # exactly the TTL: expired
cache.get("a", load)
print(calls)                                 # ['a', 'a']
```

The injected clock lets the test move time without sleeping. An entry is dead at exactly the TTL, and a failing `load` stores nothing. Eviction is oldest-insert; a true LRU also refreshes on read.

## What to say in the interview

"I use a cache when the value is expensive and can be slightly stale, and I choose the TTL from how fast the source changes. I inject the clock so tests control time, I use a monotonic clock in production, I never cache errors, and I bound the size. For hot keys I would add request coalescing or a random jitter on the TTL so they do not all expire together."
