---
title: "Lists: append, extend, insert, pop, in, copy"
summary: Add, remove, find and copy items in a list, and know which methods change it in place.
tags: [python, lists]
---
```python
xs = [3, 1]
xs.append(2)         # xs is [3, 1, 2]           one item at the end
xs.extend([5, 4])    # xs is [3, 1, 2, 5, 4]     every item of an iterable
xs.insert(0, 9)      # xs is [9, 3, 1, 2, 5, 4]  before index 0
xs.pop()             # 4   removes and returns the last item
xs.pop(0)            # 9   removes and returns the item at index 0
2 in xs              # True
ys = xs.copy()       # a separate list with the same items
```

- `append`, `extend`, `insert`, `remove`, `sort` and `reverse` change the list and return `None`.
- `ys = xs` does not copy. Both names point to the same list.
- `in` scans the whole list. For many lookups use a set.

<!-- more -->

## Details

Other useful operations:

```python
xs = [3, 1, 2, 1]
xs.remove(1)         # xs is [3, 2, 1]   first matching value, ValueError if missing
xs.index(2)          # 1                 position of a value, ValueError if missing
xs.count(1)          # 1
del xs[0]            # xs is [2, 1]
len(xs), sum(xs), min(xs), max(xs)   # (2, 3, 1, 2)
xs + [7]             # [2, 1, 7]         a new list, xs unchanged
[0] * 3              # [0, 0, 0]
```

`pop()` on an empty list raises `IndexError`. Check `if xs:` first.

`append` and `pop()` at the end are fast. `insert(0, x)` and `pop(0)` shift every item, so they are slow on long lists. Use `collections.deque` for a queue.

`copy()`, `xs[:]` and `list(xs)` all make a shallow copy: the outer list is new, but nested lists are still shared.

Multiplying a nested list repeats the same inner list:

```python
grid = [[0] * 2] * 2
grid[0][0] = 1
grid                 # [[1, 0], [1, 0]]   both rows are one list
grid = [[0] * 2 for _ in range(2)]   # correct: two separate rows
```

## Common mistakes

- Writing `xs = xs.append(1)`. This sets `xs` to `None`.
- Using `append` with a list when you want its items: `[1].append([2, 3])` gives `[1, [2, 3]]`. Use `extend`.
- Removing items from a list while looping over it. Build a new list instead.
- Treating `ys = xs` as a copy, then being surprised when both change.

## See also

- [Slicing](#/kb/py-slicing)
- [List comprehensions](#/kb/py-list-comprehensions)
- [Mutability, aliasing and copying](#/kb/py-copy-mutability)
- [deque and OrderedDict](#/kb/py-collections-deque)
- Official docs: https://docs.python.org/3/tutorial/datastructures.html
