---
title: Counter and defaultdict
summary: Count items with Counter and group items with defaultdict, without checking for missing keys.
tags: [python, dicts, collections]
---
```python
from collections import Counter, defaultdict
c = Counter("banana")              # Counter({'a': 3, 'n': 2, 'b': 1})
c["a"], c["z"]                     # (3, 0)    a missing key counts as 0
c.most_common(2)                   # [('a', 3), ('n', 2)]
groups = defaultdict(list)         # a missing key starts as list()
for w in ["apple", "avocado", "bean"]:
    groups[w[0]].append(w)
dict(groups)                       # {'a': ['apple', 'avocado'], 'b': ['bean']}
```

- `Counter(iterable)` counts hashable items. It is a dict, so `.items()`, `in` and `len` all work.
- `defaultdict(factory)` calls `factory()` to create the value the first time a key is used.
- Common factories: `list` for grouping, `int` for counting, `set` for unique members.

<!-- more -->

## Details

A `Counter` can be updated after it is built:

```python
c = Counter(["x", "y", "x"])
c["y"] += 1                        # c is Counter({'x': 2, 'y': 2})
c.update(["x", "z"])               # c is Counter({'x': 3, 'y': 2, 'z': 1})
c.total()                          # 6
c.most_common(1)                   # [('x', 3)]
```

`most_common(k)` returns `(item, count)` pairs, highest count first. Items with the same count come in the order they were first seen, not in alphabetical order. For a different tie rule, sort yourself: `sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))`.

Counters compare and subtract:

```python
Counter("listen") == Counter("silent")   # True    same letters, same counts
Counter("aab") - Counter("ab")           # Counter({'a': 1})   only positive counts are kept
```

`defaultdict(int)` counts in the same way as the `get` pattern:

```python
seen = defaultdict(int)
for ch in "abca":
    seen[ch] += 1
dict(seen)                         # {'a': 2, 'b': 1, 'c': 1}
```

Reading a missing key from a `defaultdict` inserts it. Reading one from a `Counter` returns 0 and inserts nothing.

```python
"q" in seen, seen["q"], "q" in seen      # (False, 0, True)
```

## Common mistakes

- Writing `defaultdict(0)` or `defaultdict([])`. The argument must be callable: `int`, `list`.
- Testing membership with `d[key]` on a `defaultdict`. It creates the key. Use `key in d`.
- Assuming `most_common` breaks ties alphabetically.
- Counting unhashable items such as lists. Convert them to tuples first.

## See also

- [Dictionaries: get, setdefault, items, membership](#/kb/py-dicts)
- [Hash map counting and lookup](#/kb/algo-hash-map-counting)
- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- Official docs: https://docs.python.org/3/library/collections.html
