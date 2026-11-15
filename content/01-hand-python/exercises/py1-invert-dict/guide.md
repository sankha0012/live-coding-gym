**Why this matters.** Swapping keys and values looks like a one-liner, but values can repeat. Several keys can share one value, so the inverse has to hold a list of keys, not a single key.

**How we get there.**
1. The tempting `{v: k for k, v in d.items()}` is wrong: when two keys have the same value, the later key silently replaces the earlier one and data is lost.
2. So collect instead. Loop over `d.items()` and for each pair use `out.setdefault(value, []).append(key)`. The first time we see a value it gets a fresh list.
3. At this point every value maps to all its keys, but in dict order, which is not what the problem wants.
4. Sort each list in a final step: `{value: sorted(keys) for value, keys in out.items()}`. Now the output is the same every time.

**Check it.** An empty dict gives an empty dict. We touch every item once and sort the lists, so the worst case is `O(n log n)`.

**Watch out.** The silent key loss of the one-line comprehension: it runs without error and returns plausible but incomplete data.
