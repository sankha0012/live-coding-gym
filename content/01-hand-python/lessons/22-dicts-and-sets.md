# Dicts and sets

## The problem it solves

Counting, grouping, looking things up by key and comparing two collections are the core of data tasks. A dict gives you lookup in constant time. A set gives you membership and comparison in constant time. If your first idea is a nested loop, a dict or set is usually the better idea.

## The smallest runnable example

```python
from collections import Counter, defaultdict

words = ["b", "a", "b", "c", "b", "a"]

counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1       # get with a default
print(counts)                              # {'b': 3, 'a': 2, 'c': 1}

print(Counter(words).most_common(2))       # [('b', 3), ('a', 2)]

groups = defaultdict(list)
for w in ["apple", "fig", "pear", "kiwi"]:
    groups[len(w)].append(w)
print(dict(groups))                        # {5: ['apple'], 3: ['fig'], 4: ['pear', 'kiwi']}

for key, value in counts.items():          # loop over pairs
    pass
print(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))
print("a" in counts, counts.get("z"), counts.get("z", 0))
```

The sort line is worth memorising: count descending, then name ascending, with the negative sign on the number. It is the answer to most "top n, ties alphabetical" prompts.

## Sets

```python
a = {1, 2, 3}
b = {3, 4}
print(a & b, a | b, a - b, a ^ b)   # {3} {1, 2, 3, 4} {1, 2} {1, 2, 4}
print(set([1, 1, 2]), 2 in a)
print(sorted(a - b))                # sets have no order: sort to print
```

`a - b` is "in a but not in b". For a report of added, removed and kept between an old and a new collection, that is three set operations. Convert a list to a set for fast membership checks: `x in some_list` scans the whole list, `x in some_set` does not.

## Merging two dicts and summing values

```python
a = {"x": 1, "y": 2}
b = {"y": 10, "z": 5}
out = dict(a)
for k, v in b.items():
    out[k] = out.get(k, 0) + v
print(out)   # {'x': 1, 'y': 12, 'z': 5}
```

The expression `{**a, **b}` merges too, but the second dict wins on a clash instead of summing. Know which one the prompt wants.

## Trap 1: `d[key]` on a missing key

```python
d = {"a": 1}
try:
    d["b"]
except KeyError as e:
    print("KeyError", e)
print(d.get("b"))   # None
```

Use `get` with a default, or `defaultdict`, or test `if key in d`. Do not wrap everything in a bare `except`.

## Trap 2: changing a dict while looping over it

```python
d = {"a": 1, "b": 2}
try:
    for k in d:
        d[k + "x"] = 0
except RuntimeError as e:
    print(e)        # dictionary changed size during iteration
for k in list(d):   # loop over a copy of the keys instead
    d[k + "y"] = 0
print(len(d))
```

Loop over `list(d)` or build a new dict.

## Trap 3: unhashable keys and the empty `{}`

Lists and dicts cannot be keys or set members. Use a tuple: `seen.add((x, y))`. Also, `{}` is an empty dict, not an empty set. Write `set()` for an empty set.

```python
seen = set()
seen.add((1, 2))
print((1, 2) in seen, type({}), type(set()))
```

## Inverting a dict whose values repeat

```python
def invert(d):
    out = {}
    for k, v in d.items():
        out.setdefault(v, []).append(k)
    return out

print(invert({"a": 1, "b": 2, "c": 1}))   # {1: ['a', 'c'], 2: ['b']}
```

`setdefault(v, [])` returns the existing list or inserts a new one. It is the dict version of "create the group if missing, then append".

## Order

Since Python 3.7 a dict keeps insertion order. A set does not promise any order. When the prompt asks for sorted output, call `sorted` yourself and do not rely on luck.

## Say it like this

"I use a dict to count, so each item is looked up in constant time and the whole thing is linear in the input. For the top n I sort by count descending and then by name, so ties are stable and alphabetical. I use sets for added, removed and kept, which avoids a nested loop. For missing keys I use get with a default, so there is no KeyError."
