Write a class `Counter` that counts items.
- `add(item, k=1)` adds `k` to the count of `item`.
- `count(item)` returns the count, or 0 for an item never added.
- `total()` returns the sum of all counts.
- `most_common(n)` returns a list of `(item, count)` tuples, the `n` highest counts first. Items with the same count are ordered by item, from smallest to largest. If `n` is larger than the number of items, return all of them. An empty counter returns `[]`.
Items are always strings.
