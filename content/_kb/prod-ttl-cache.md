---
title: Caches with a TTL
summary: Store a value with an expiry time and reload it when it is missing or too old.
tags: [production, caching]
---
```python
class TTLCache:
    def __init__(self, ttl, clock):
        self.ttl, self.clock, self.data = ttl, clock, {}    # key -> (value, expires_at)

    def get(self, key, load):
        hit = self.data.get(key)
        if hit is not None and self.clock() < hit[1]:
            return hit[0]                                   # fresh
        value = load(key)                                   # missing or expired
        self.data[key] = (value, self.clock() + self.ttl)
        return value
```

- Use it for slow lookups that may be slightly old: features, model metadata, config.
- Key rule: store the expiry next to the value and compare it with an injected clock on every read.
- Say: "The TTL is the staleness I accept. A longer TTL means fewer loads and older data."

<!-- more -->

## Details

```python
t, loads = [0.0], []
cache = TTLCache(ttl=60, clock=lambda: t[0])

def load(key):
    loads.append(key)
    return key.upper()

cache.get("a", load)     # 'A'
cache.get("a", load)     # 'A'
loads                    # ['a']       the second call was a hit
t[0] = 60.0
cache.get("a", load)     # 'A'
loads                    # ['a', 'a']  expired exactly at the TTL, loaded again
```

The entry is a tuple, so a cached value of `None` or `0` is still a hit. The test is on the tuple, not on the value.

**Eviction.** This cache removes nothing. An expired key stays in memory until it is read again. For many keys, add a size limit (an LRU) or sweep expired entries from time to time.

**Failures.** If `load` raises, nothing is stored and the error goes up. Two useful variants: cache the failure for a short time so a broken source is not hit on every request, or serve the old value when the reload fails ("stale on error").

**Invalidation.** When you know the source changed, delete the key. Do not wait for the TTL.

With many threads, an expired hot key makes all of them reload at once. A lock per key avoids that.

## Common mistakes

- Writing `if cache.get(key):` so falsy values are reloaded every time.
- Mixing `<` and `<=` at the expiry boundary. Decide whether an entry is valid at exactly `expires_at`.
- Using `time.time()` directly, so the test must sleep to see an expiry.
- Storing the time of the write and forgetting to compare it on read.
- Caching without any size bound for keys that come from user input.

## See also

- [LRU cache](#/kb/algo-lru-cache)
- [Clocks: time.monotonic and injecting a clock or sleep](#/kb/py-time-clock-injection)
- [Fallbacks and fallback chains](#/kb/prod-fallbacks)
