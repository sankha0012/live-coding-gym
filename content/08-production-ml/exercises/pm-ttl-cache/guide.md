**Why this matters.** A scoring service caches feature lookups, but old values go stale and memory is limited, so entries need an expiry and a size cap. Time comes from an injected `clock`.

**How we get there.**
1. Store `key -> (value, stored_at)` in a dict; insertion order makes the first key the oldest set.
2. Write `_purge`: take `now = self.clock()` and delete entries where `now - t >= ttl_s`. Exactly at the TTL counts as expired.
3. Call `_purge` at the start of `get`, `set` and `__len__`, so expired entries are never seen.
4. In `set`, first `pop(key, None)`. That makes a replacement restart its age by moving it to the end, and it never evicts a neighbour.
5. If the cache is still full, delete `next(iter(self._data))`, the oldest entry, then store the new tuple with `clock()`.

**Check it.** `get` does not refresh the age. A cached `None` is still a hit. Each call purges in O(n), fine for a small cache.

**Watch out.** Expiring with `>` instead of `>=`, keeping the old timestamp when a key is replaced, or reading the real time instead of `clock` are the mistakes this is built to catch.
