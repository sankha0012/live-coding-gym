---
title: Loops with enumerate, zip and range
summary: Loop over numbers with range, over items with their index using enumerate, and over several lists at once with zip.
tags: [python, loops, iteration]
---
```python
names, ages = ["ana", "bo"], [31, 25]
list(range(3))                     # [0, 1, 2]        stop is excluded
list(range(2, 10, 3))              # [2, 5, 8]        start, stop, step
list(range(3, 0, -1))              # [3, 2, 1]        counting down
list(enumerate(names))             # [(0, 'ana'), (1, 'bo')]
list(enumerate(names, start=1))    # [(1, 'ana'), (2, 'bo')]
list(zip(names, ages))             # [('ana', 31), ('bo', 25)]
dict(zip(names, ages))             # {'ana': 31, 'bo': 25}
```

- Loop over the items directly: `for name in names:`. Use `enumerate` when you also need the index.
- `zip` stops at the shortest input without any error.
- `range`, `enumerate` and `zip` are lazy. Wrap them in `list()` to see the values.

<!-- more -->

## Details

In a `for` loop, unpack the pairs straight into names:

```python
for i, name in enumerate(names, start=1):
    print(i, name)                 # 1 ana   then   2 bo
for name, age in zip(names, ages):
    print(name, age)               # ana 31  then   bo 25
```

Useful `zip` patterns:

```python
xs = [1, 2, 3]
list(zip(xs, xs[1:]))              # [(1, 2), (2, 3)]   neighbouring pairs
list(zip(*[[1, 2], [3, 4]]))       # [(1, 3), (2, 4)]   columns of a grid
list(zip(xs, "ab"))                # [(1, 'a'), (2, 'b')]   3 is dropped
list(reversed(xs))                 # [3, 2, 1]
```

`zip(a, b, strict=True)` raises `ValueError` when the lengths differ. Use it when a silent cut would hide a bug.

`break` leaves the loop. `continue` jumps to the next item. A `for ... else` block runs only when the loop finished without `break`:

```python
for x in xs:
    if x > 5:
        break
else:
    print("none above 5")          # none above 5
```

Use `while condition:` when you do not know the number of rounds in advance. Make sure something inside the loop changes the condition.

A `zip` or `enumerate` object can be read only once. After one full loop it is empty.

## Common mistakes

- Writing `for i in range(len(xs)):` only to read `xs[i]`. Loop over `xs` or use `enumerate`.
- Off-by-one with `range`: `range(1, n)` stops at `n - 1`.
- Losing data because `zip` cut the longer list.
- Reusing a `zip` object after it was consumed.

## See also

- [List comprehensions](#/kb/py-list-comprehensions)
- [Tuples and unpacking](#/kb/py-tuples-unpacking)
- [Iterators and generators](#/kb/py-iterators-generators)
- Official docs: https://docs.python.org/3/library/functions.html
