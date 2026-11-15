Let a single entry have its own lifetime. Change `set` so it takes an optional third argument: `set(key, value, ttl_s=None)`.

- `cache.set("a", 1, 2)` stores `a` with a lifetime of 2 seconds. That entry is expired when `clock() - stored_at >= 2`, whatever the cache-wide `ttl_s` is.
- `cache.set("b", 2)` or `cache.set("b", 2, None)` keeps using the cache-wide `ttl_s`, exactly as before.
- Replacing a key sets its lifetime again from the new call, so a plain `set("a", 3)` after `set("a", 1, 2)` goes back to the cache-wide `ttl_s`.

Everything else stays the same. Example with `TTLCache(10, 5, clock)`: after `set("a", 1, 2)` and `set("b", 2)`, three seconds later `get("a")` is `None` and `get("b")` is `2`.
