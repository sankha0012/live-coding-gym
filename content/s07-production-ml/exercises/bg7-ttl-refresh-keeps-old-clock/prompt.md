A scoring service caches feature lookups. Write a class `TTLCache(ttl_s, max_size, clock)`.

- `clock` is a function that returns the current time in seconds. Always use it, never the real time.
- `set(key, value)` stores the value with the time `clock()`. Setting an existing key replaces the value and restarts its TTL.
- `get(key, default=None)` returns the value, or `default` if the key is missing or expired.
- An entry is expired when `clock() - stored_at >= ttl_s` (at exactly `ttl_s` seconds it is already expired).
- `len(cache)` counts only entries that are not expired.
- The cache never holds more than `max_size` live entries. When `set` adds a new key and the cache is full, first drop expired entries, and if it is still full, evict the entry with the oldest `set` time (the oldest insertion or refresh). Replacing an existing key never evicts another key.
- `max_size < 1` raises `ValueError`.
- A stored value of `None` is a real value: `get` returns it, it is not "missing".

An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
