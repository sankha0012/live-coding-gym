**Why this matters.** A ranking that changes order between runs, when scores tie, makes reports flip around and breaks comparisons. We want one defined order for every input, including missing scores.

**How we get there.**
1. Use `sorted(records, key=...)`, not `.sort()`. It returns a new list, so the caller's list and dicts stay as they were.
2. The key is a tuple, and Python compares tuple items left to right. First item: `r["score"] is None`. `False` sorts before `True`, so missing scores go last, and we never compare `None` with a number.
3. Second item: `-(r["score"] or 0)`. Negating puts higher scores first without `reverse=True`. The `or 0` only matters for `None`, which the first item has already moved to the end.
4. Third item: `r["id"]`, so equal scores are ordered alphabetically.
5. If everything in the key is equal, `sorted` is stable, so those records keep their input order.

**Check it.** An empty list returns `[]`. The cost is O(n log n).

**Watch out.** `reverse=True` also reverses the id order, and `-r["score"]` crashes on `None`; testing the score for truthiness would also mix up a real `0`.
