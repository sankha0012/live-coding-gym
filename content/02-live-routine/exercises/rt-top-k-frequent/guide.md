**Why this matters.** "Most common things" is a standard analytics question. The twist is the tie rule: equal counts must come out in the order they first appeared, and it is easy to break that by accident.
**How we get there.**
1. Count with `Counter(items)`. It is a dict, and dicts remember the order keys were first inserted, so the counts come out in first-appearance order.
2. Sort the distinct items by count, highest first: `sorted(counts, key=lambda x: -counts[x])`. We sort the keys, not the original list, so each item appears once.
3. Python's sort is stable. Items with equal keys keep their relative order, so ties stay in first-appearance order with no extra code.
4. Slice the first k: `ordered[:k]`.
**Check it.** `k = 0` gives an empty slice, a `k` larger than the number of distinct items just returns them all, and an empty input gives `[]`. Counting is O(n) and sorting is O(d log d) for d distinct items.
**Watch out.** Sorting by `(-count, x)` breaks ties alphabetically instead of by first appearance, and sorting the raw list returns duplicates.
