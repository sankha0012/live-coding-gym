**Why this matters.** Comparing "before" and "after" lists, such as users, files or permissions, comes down to what was added, removed and kept. Sets are made for exactly this.

**How we get there.**
1. Turn both lists into sets: `o, n = set(old), set(new)`. This removes duplicates at the same time.
2. Added is what is in `new` but not in `old`: `n - o`.
3. Removed is the reverse: `o - n`. Kept is what is in both: `o & n`.
4. Sets have no guaranteed order, so wrap each result in `sorted(...)`. That also turns it into the list the problem asks for.
5. Put the three lists in a dict under `"added"`, `"removed"` and `"kept"`.

**Check it.** Two empty lists give three empty lists. Building the sets and doing the operations is linear, and sorting makes the total `O(n log n)`.

**Watch out.** Returning raw sets, or sorting nothing, gives output whose order cannot be relied on, and looping with `in` over lists instead of sets gets slow.
