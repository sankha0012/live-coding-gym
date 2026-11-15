**Why this matters.** Two orders end up sharing one tag list, so a "new" tag appears on a "vip" customer. This is the best-known Python trap: a default value is created once, when the function is defined, not on every call.

**How we get there.**
1. Reproduce. Tagging `a` "vip" then `b` "new" returns both tags for `b`.
2. Locate it. `tags=[]` is built once and every call that omits the argument gets that same list object. Appending changes the shared list.
3. Fix it with the usual pattern: default to `None`, and inside the function write `if tags is None: tags = []`. Now every call gets a fresh list.
4. Move to the second bug. Sorting by `counts[r]` is ascending, so the least busy restaurants come first.
5. We want most orders first, ties by smaller id. A tuple key does both: `key=lambda r: (-counts[r], r)`. The minus flips the count and the id breaks ties upward.

**Check it.** Ties come out in id order. Sorting is O(k log k).

**Watch out.** A mutable default looks harmless and passes a single test. Whenever you see `=[]` or `={}` in a signature, treat it as a bug.
