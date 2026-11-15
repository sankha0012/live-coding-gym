---
title: Sets and set operations
summary: A set holds unique items with fast membership tests, plus union, intersection and difference.
tags: [python, sets]
---
```python
a, b = {1, 2, 3}, {3, 4}
a | b              # {1, 2, 3, 4}   union: in either
a & b              # {3}            intersection: in both
a - b              # {1, 2}         difference: in a, not in b
a ^ b              # {1, 2, 4}      in exactly one of them
2 in a             # True           fast, even for a large set
a.add(5); a.discard(9)              # discard never raises
len(set("hello"))  # 4              number of distinct letters
```

- A set has no duplicates, no order and no indexing.
- `set()` is the empty set. `{}` is an empty dict.
- Items must be hashable: numbers, strings, tuples. Not lists or dicts.

<!-- more -->

## Details

Membership in a set takes constant time on average. In a list it scans every item. Convert a list to a set before testing many values against it.

The "seen" pattern finds repeats in one pass:

```python
seen = set()
for x in [3, 1, 3]:
    if x in seen:
        print("repeat", x)          # repeat 3
    seen.add(x)
```

`set(xs)` removes duplicates but loses the order. To keep the first occurrence of each item in order, use a dict:

```python
xs = [3, 1, 3, 2]
sorted(set(xs))                     # [1, 2, 3]   unique and sorted
list(dict.fromkeys(xs))             # [3, 1, 2]   unique, original order
```

Comparisons test for subsets:

```python
{1, 2} <= {1, 2, 3}                 # True    subset
{1, 2}.isdisjoint({3})              # True    nothing in common
{1, 2} == {2, 1}                    # True    order does not matter
```

`remove(x)` raises `KeyError` when `x` is missing. `discard(x)` does nothing. `a.update(b)` or `a |= b` adds every item of `b` to `a`. The method forms `a.union(b)`, `a.intersection(b)` and `a.difference(b)` accept any iterable, while the operators need sets on both sides.

A `frozenset` is an immutable set. It can be a dict key or a member of another set.

## Common mistakes

- Creating an empty set with `{}`.
- Expecting a set to keep insertion order, or printing a set where the order is checked.
- Indexing a set: `s[0]` raises `TypeError`. Convert with `sorted(s)` or `list(s)`.
- Adding a list to a set: `TypeError: unhashable type`. Use a tuple.

## See also

- [Dict and set comprehensions](#/kb/py-dict-comprehensions)
- [Dictionaries: get, setdefault, items, membership](#/kb/py-dicts)
- [Big-O of common Python operations](#/kb/py-complexity)
- Official docs: https://docs.python.org/3/library/stdtypes.html
