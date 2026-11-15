**Why this matters.** A full cache must decide what to throw away. Least recently used is the usual rule: if you have not touched something in a while, you probably will not need it soon.
**How we get there.**
1. We need two things at O(1): look up a key, and know which key is oldest. A dict gives the first, an `OrderedDict` also remembers order, which gives the second.
2. Keep the order from oldest at the front to newest at the back.
3. In `get`, a missing key returns `-1`. Otherwise `move_to_end(key)` marks it as just used, then return the value. Reading counts as use.
4. In `put`, set the value and `move_to_end(key)`, so both new and updated keys become the newest.
5. If the size now exceeds `capacity`, remove the oldest with `popitem(last=False)`. Updating an existing key does not grow the size, so nothing goes.
**Check it.** With capacity 1, each new key replaces the previous one. Every operation is O(1). By hand, it is a dict plus a doubly linked list.
**Watch out.** A `get` that does not refresh the key, or evicting the newest instead of the oldest, makes the cache forget the wrong thing.
