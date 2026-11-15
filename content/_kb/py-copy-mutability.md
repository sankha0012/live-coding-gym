---
title: Mutability, aliasing and copying
summary: Assignment never copies. Two names can share one list, and a shallow copy still shares nested items.
tags: [python, mutability, copying]
---
```python
import copy
a = [1, 2, 3]
b = a                  # no copy: b is another name for the same list
b.append(4)            # a is now [1, 2, 3, 4] too
c = a.copy()           # shallow copy: a new outer list (also a[:] or list(a))
grid = [[0] * 2 for _ in range(2)]   # correct: two separate rows
bad = [[0] * 2] * 2                  # wrong: the same row twice
bad[0][0] = 1          # bad is [[1, 0], [1, 0]]
deep = copy.deepcopy(grid)           # copies nested lists as well
```

- Mutable: `list`, `dict`, `set`. Immutable: `int`, `float`, `str`, `tuple`, `frozenset`, `None`.
- `=` binds a name to an object. It never makes a copy.
- A shallow copy duplicates the outer container only. Use `copy.deepcopy` for nested data.

<!-- more -->

## Details

A shallow copy shares the inner objects:

```python
nested = [[1], [2]]
shallow = nested.copy()
shallow[0].append(9)       # nested is now [[1, 9], [2]]
shallow.append([3])        # nested is unchanged by this
```

`dict(d)`, `d.copy()` and `set(s)` are shallow in the same way.

Functions receive the same object, not a copy. Changing it in place is visible to the caller. Rebinding the name is not:

```python
def add_in_place(xs):
    xs.append(1)           # caller sees this

def rebind(xs):
    xs = xs + [1]          # new local list, caller sees nothing

z = []
add_in_place(z); rebind(z)
z                          # [1]
```

A mutable default value is created once and shared by every call:

```python
def add(x, xs=[]):
    xs.append(x)
    return xs

add(1)    # [1]
add(2)    # [1, 2]   the same list again
```

Use `xs=None` and create the list inside the function.

`+=` on a list changes it in place, so aliases see it. `xs = xs + [...]` makes a new list. Strings are immutable, so `s += "c"` always makes a new string.

Methods that change a list in place return `None`: `sort`, `reverse`, `append`, `extend`. `sorted(xs)` returns a new list.

Only immutable (hashable) values can be dict keys or set items. A list as a key raises `TypeError: unhashable type: 'list'`. Use a tuple.

## Common mistakes

- Writing `[[0] * n] * m` for a grid. All rows are the same list.
- Writing `xs = xs.sort()`. Now `xs` is `None`.
- Using `.copy()` on nested data and still changing the original.
- Removing items from a list while looping over it. Loop over a copy (`for v in xs[:]`) or build a new list.

## See also

- [Lists: append, extend, insert, pop, in, copy](#/kb/py-lists)
- [Functions: defaults, *args, **kwargs, the mutable default trap](#/kb/py-functions-args)
- [Truthiness, None and "is" versus "=="](#/kb/py-truthiness-none)
- [Grids and matrices](#/kb/algo-matrix)
- Official docs: https://docs.python.org/3/library/copy.html
