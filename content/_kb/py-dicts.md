---
title: "Dictionaries: get, setdefault, items, membership"
summary: Store and look up values by key, handle missing keys safely, and loop over keys and values.
tags: [python, dicts]
---
```python
d = {"a": 1, "b": 2}
d["a"]                # 1      KeyError if the key is missing
d.get("z")            # None   no error
d.get("z", 0)         # 0      your own default
d["c"] = 3            # add or overwrite
"a" in d              # True   tests keys, not values
d.pop("a")            # 1      remove and return
d.setdefault("xs", []).append(5)    # d is {'b': 2, 'c': 3, 'xs': [5]}
for key, value in d.items(): ...    # loop over pairs
```

- `d[key]` raises `KeyError` for a missing key. `d.get(key, default)` never raises.
- `get` does not store anything. `setdefault` stores the default when the key is missing.
- A dict keeps insertion order.

<!-- more -->

## Details

The counting pattern with `get`:

```python
counts = {}
for ch in "banana":
    counts[ch] = counts.get(ch, 0) + 1
counts                          # {'b': 1, 'a': 3, 'n': 2}
max(counts, key=counts.get)     # 'a'    key with the largest value
```

Looping over a dict gives its keys. `d.keys()`, `d.values()` and `d.items()` are live views. Wrap them in `list()` when you need a real list.

```python
d = {"a": 1, "b": 2}
list(d)                 # ['a', 'b']
list(d.values())        # [1, 2]
d.update({"b": 20, "c": 3})   # d is {'a': 1, 'b': 20, 'c': 3}
d | {"z": 0}            # {'a': 1, 'b': 20, 'c': 3, 'z': 0}   new dict
d.pop("nope", None)     # None   a default avoids the KeyError
del d["a"]              # d is {'b': 20, 'c': 3}
```

Keys must be hashable: strings, numbers and tuples work, lists and dicts do not. Lookup, insert and delete by key take constant time on average.

Two dicts are equal when they hold the same pairs. Order does not matter for `==`.

## Common mistakes

- Writing `d[key] += 1` before the key exists: `KeyError`.
- Testing `if d.get(key):` when a stored value can be `0` or `""`. Use `if key in d:`.
- Adding or removing keys while looping over the dict: `RuntimeError`. Loop over `list(d)`.
- Using `value in d` and expecting it to search the values. Use `value in d.values()`.

## See also

- [Counter and defaultdict](#/kb/py-counter-defaultdict)
- [Dict and set comprehensions](#/kb/py-dict-comprehensions)
- [Hash map counting and lookup](#/kb/algo-hash-map-counting)
- Official docs: https://docs.python.org/3/library/stdtypes.html
