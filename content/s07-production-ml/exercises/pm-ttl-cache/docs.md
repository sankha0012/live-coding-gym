# TTLCache: reference

## Contract

`TTLCache(ttl_s, max_size, clock)`. `clock()` returns the current time in seconds and is the only source of time.

- `set(key, value)` stores the value with timestamp `clock()`. Setting an existing key replaces the value and restarts its TTL.
- `get(key, default=None)` returns the stored value, or `default` when the key is missing or expired. A stored `None`, `0` or `""` is a real value and is returned.
- An entry is expired when `clock() - stored_at >= ttl_s`, so at exactly `ttl_s` seconds it is already gone.
- `len(cache)` counts only live entries, even if no `get` or `set` happened since they expired.
- The cache never holds more than `max_size` live entries. When a new key is added to a full cache, expired entries go first. If it is still full, the entry with the oldest `set` time is evicted. Replacing an existing key never evicts another key.
- `get` does not refresh age. `max_size < 1` raises `ValueError`.

```python
c = TTLCache(10, 2, clock)
c.set("a", 1)          # at t=100
c.get("a")             # 1 at t=109.9, None at t=110
```

## Library notes

- `dict.get(key, default)` returns `default` for a missing key. Gotcha: a stored `None` looks the same as missing, so test membership with `key in d` or use a private sentinel `object()`.
- `collections.OrderedDict.move_to_end(key, last=True)` returns `None` and reorders in place. Gotcha: it raises `KeyError` for an absent key.
- `min(iterable, key=fn)` returns the smallest item. Gotcha: it raises `ValueError` on an empty iterable.

## Gotchas

- The real `time.time()` jumps when the wall clock is adjusted. Inject `time.monotonic` in production.
- Purging expired entries only on `get` lets never-read keys grow without bound.
- Not thread-safe by itself. A service with worker threads needs a lock around `set`.
