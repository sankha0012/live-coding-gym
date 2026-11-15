---
title: Dict and set comprehensions
summary: "Build a dict with {key: value for ...} or a set with {value for ...} in one expression."
tags: [python, dicts, comprehensions]
---
```python
words = ["fig", "apple", "fig"]
{w: len(w) for w in words}                    # {'fig': 3, 'apple': 5}   repeated keys overwrite
{len(w) for w in words}                       # {3, 5}                   no colon: a set
prices = {"a": 5, "b": 12}
{k: v for k, v in prices.items() if v > 10}   # {'b': 12}                filter a dict
{v: k for k, v in prices.items()}             # {5: 'a', 12: 'b'}        swap keys and values
{i: w for i, w in enumerate(words)}           # {0: 'fig', 1: 'apple', 2: 'fig'}
```

- A colon between key and value makes a dict. No colon makes a set.
- A key can appear only once. The last value written for it wins.
- `{}` is an empty dict. An empty set is `set()`.

<!-- more -->

## Details

The shape is the same as a list comprehension, with curly braces: `{key_expr: value_expr for item in iterable if condition}`.

To loop over an existing dict, use `.items()` and unpack the pair. Looping over the dict itself gives only the keys.

```python
{k: v * 2 for k, v in prices.items()}         # {'a': 10, 'b': 24}
{k.upper(): v for k, v in prices.items()}     # {'A': 5, 'B': 12}
```

Two lists of the same length become a dict with `zip`. For a plain pairing, `dict(zip(...))` is shorter than a comprehension:

```python
keys, vals = ["x", "y"], [1, 2]
dict(zip(keys, vals))                         # {'x': 1, 'y': 2}
{k: v for k, v in zip(keys, vals) if v > 1}   # {'y': 2}
dict.fromkeys(keys, 0)                        # {'x': 0, 'y': 0}
```

A set comprehension removes duplicates as it builds. A set has no order, so sort it when the order matters:

```python
sorted({w[0] for w in words})                 # ['a', 'f']
```

A comprehension writes one value per key. It cannot collect several values under the same key. For grouping or counting, use a loop with `defaultdict` or `Counter`.

## Common mistakes

- Swapping keys and values when values repeat: the duplicates are silently lost.
- Writing `{}` and expecting an empty set.
- Using `dict.fromkeys(keys, [])`: every key shares the same list. Write `{k: [] for k in keys}`.
- Forgetting `.items()` and trying to unpack keys: `for k, v in prices` fails.
- Relying on the order of a set.

## See also

- [List comprehensions](#/kb/py-list-comprehensions)
- [Dictionaries: get, setdefault, items, membership](#/kb/py-dicts)
- [Sets and set operations](#/kb/py-sets)
- [Counter and defaultdict](#/kb/py-counter-defaultdict)
- Official docs: https://docs.python.org/3/tutorial/datastructures.html
