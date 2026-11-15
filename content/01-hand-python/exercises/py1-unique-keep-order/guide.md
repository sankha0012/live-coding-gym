**Why this matters.** Removing duplicates is easy with a set, but a set forgets order. The real task is keeping the first appearance of each item, in the original order.

**How we get there.**
1. We need to remember what we have already seen. A set is perfect: checking `x in seen` takes constant time on average.
2. Make two containers: `seen = set()` for the check and `out = []` for the answer, because the list keeps the order.
3. Walk the items in order. If `x` is not in `seen`, it is the first time, so do both `seen.add(x)` and `out.append(x)`.
4. If it is already in `seen`, do nothing. Return `out`.

**Check it.** An empty list gives an empty list. Time and space are linear. Using `x in out` instead of the set would work but scan the list each time, making it quadratic.

**Watch out.** `list(set(items))` removes duplicates but can scramble the order. Items must be hashable to go in a set.
