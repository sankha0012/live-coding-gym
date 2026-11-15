---
title: Tuples and unpacking
summary: A tuple is a fixed, immutable sequence; unpacking assigns its items to several names at once.
tags: [python, tuples, unpacking]
---
```python
t = (1, "a")                # a tuple; (1,) is a tuple with one item
x, y = t                    # x is 1, y is 'a'
a, b = 1, 2
a, b = b, a                 # swap: a is 2, b is 1
first, *rest = [1, 2, 3]    # first is 1, rest is [2, 3]
head, *_, last = "abcd"     # head is 'a', last is 'd'
for name, (lo, hi) in [("x", (0, 9))]: ...   # nested unpacking in a loop
```

- The comma makes the tuple, not the parentheses: `(1)` is the int 1, `(1,)` is a tuple.
- Unpacking works on any iterable. The number of names must match the number of items.
- One starred name collects the leftover items into a list.

<!-- more -->

## Details

A tuple supports indexing, slicing, `len`, `in` and loops, like a list. It cannot be changed: `t[0] = 5` raises `TypeError`, and there is no `append`.

Because a tuple is immutable it is hashable, so it can be a dict key or a set member:

```python
visits = {(0, 0): "start", (2, 3): "end"}
visits[(2, 3)]              # 'end'
(2, 3) in visits            # True
```

A function returns several values as one tuple. Unpack it at the call:

```python
def min_max(xs):
    return min(xs), max(xs)

lo, hi = min_max([4, 1, 9])   # lo is 1, hi is 9
q, r = divmod(17, 5)          # q is 3, r is 2
```

Tuples compare item by item, left to right. This is why tuples work well as sort keys:

```python
(1, 2) < (1, 3)             # True
(2, 0) > (1, 99)            # True    the first item decides
```

A star in a call does the opposite of unpacking in an assignment: `f(*args)` spreads a sequence into separate arguments.

A wrong count fails loudly:

```python
try:
    a, b = [1, 2, 3]
except ValueError as e:
    print(e)                # too many values to unpack (expected 2)
```

## Common mistakes

- Writing `(1)` or `("a")` and expecting a tuple.
- Unpacking a string by accident: `a, b = "hi"` works and gives two characters.
- Putting a list inside a tuple and using it as a dict key: it is no longer hashable.
- Returning a tuple and forgetting to unpack it at the call.

## See also

- [Loops with enumerate, zip and range](#/kb/py-loops-enumerate-zip)
- [Functions: defaults, *args, **kwargs, the mutable default trap](#/kb/py-functions-args)
- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- Official docs: https://docs.python.org/3/tutorial/datastructures.html
