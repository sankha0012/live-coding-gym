---
title: Hash map counting and lookup
summary: Use a dict or set to count, group, or remember what you have seen, in one O(n) pass.
tags: [algorithms, dicts, sets]
---
```python
counts = {}
for w in ["b", "a", "b"]:
    counts[w] = counts.get(w, 0) + 1          # count
counts                                        # {'b': 2, 'a': 1}
groups = {}
for name in ["ana", "bo", "al"]:
    groups.setdefault(name[0], []).append(name)   # group by a key
groups                                        # {'a': ['ana', 'al'], 'b': ['bo']}
seen = set()
for x in [3, 5, 3]:
    if x in seen: print("repeat", x)          # repeat 3
    seen.add(x)
```

- Reach for it when you hear "most frequent", "duplicates", "group by", "seen before", "in A but not in B".
- `in`, read and write on a dict or set are O(1) on average, so one pass is O(n).
- It costs O(n) extra memory. That is the usual trade: memory for time.

<!-- more -->

## Details

**Counting.** `collections.Counter` does the loop for you, and `most_common` sorts by count:

```python
from collections import Counter
c = Counter("banana")
c.most_common(2)                              # [('a', 3), ('n', 2)]
c["z"]                                        # 0   missing keys count as zero
sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:2]   # [('a', 3), ('n', 2)]
```

`most_common` leaves ties in first-seen order. When the task gives a tie rule, sort yourself with a key such as `(-count, word)`.

**Lookup.** Many slow solutions have an inner loop that searches for something. Store what you have seen in a dict, keyed by the thing you will search for, and the inner loop becomes one lookup. Typical shapes are `value -> index`, `id -> record` and `key -> latest value`.

```python
last_index = {}
for i, x in enumerate(["a", "b", "a"]):
    last_index[x] = i
last_index                                    # {'a': 2, 'b': 1}
```

Check for the partner **before** you store the current item, so an item does not match itself.

**Two dicts.** For an average per key, keep a total dict and a count dict, then divide at the end.

Keys must be hashable: strings, numbers and tuples work, lists do not. Use `tuple(xs)` or `"".join(sorted(word))` to build a key.

## Common mistakes

- `counts[w] += 1` on a plain dict raises `KeyError` for a new key. Use `.get(w, 0)`, `defaultdict(int)` or `Counter`.
- Using `x in some_list` inside a loop. That is O(n) each time. Convert to a set first.
- Expecting a set to keep order. A dict keeps insertion order, a set does not.
- Using a list as a key, which raises `TypeError: unhashable type`.

## See also

- [Counter and defaultdict](#/kb/py-counter-defaultdict)
- [Dictionaries: get, setdefault, items, membership](#/kb/py-dicts)
- [Sets and set operations](#/kb/py-sets)
- [Big-O of common Python operations](#/kb/py-complexity)
