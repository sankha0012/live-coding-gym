**Why this matters.** "Top k by frequency" is a daily analytics question. The real trap is ties: if two dishes have the same count, the answer must still be deterministic.

**How we get there.**
1. Flatten the orders while counting. Each order is a list of dishes, so `counts.update(items)` on a `Counter` adds one per dish.
2. Turn the counts into `(dish, count)` pairs with `counts.items()`.
3. Sort with a tuple key: `key=lambda kv: (-kv[1], kv[0])`. The negative count puts the biggest first, and the name breaks ties alphabetically.
4. Slice the first `k` with `ranked[:k]`, then keep only the names: `[dish for dish, _ in ranked[:k]]`.

**Check it.** An empty list gives `[]`, and a `k` larger than the number of dishes simply returns them all, because slices do not fail past the end. Counting is linear, and sorting the m distinct dishes costs O(m log m).

**Watch out.** Sorting by count alone leaves tied dishes in insertion order, which is not the alphabetical order the problem asks for.
