**Why this matters.** A cache that ignores refreshes silently returns misses for data you just wrote, and in production that shows up as extra load and stale fallbacks, not as an error.

**How we get there.**
1. Run the tests. Two fail: `test_set_again_restarts_ttl` and the replace/refresh-age test. Both involve setting the same key twice.
2. Reproduce by hand with a fake clock: `t = [0]`, `c = TTLCache(10, 5, lambda: t[0])`, `c.set("a", 1)`, `t[0] = 5`, `c.set("a", 2)`, `t[0] = 12`, then `c.get("a")`. It returns `None`, but should return `2`.
3. Read `set`. The early branch for an existing key stores `(value, self._data[key][1])`, which reuses the old timestamp, then returns.
4. Fix: remove the early branch. Pop the key first, then run the capacity check, then store `(value, self.clock())`. The solution does exactly this.

**Check it.** Rerun the tests, and make sure replacing a key in a full cache still evicts nobody.

**Watch out.** Popping before the capacity check is what keeps "replacing never evicts another key" true.
