---
title: List comprehensions
summary: Build a new list from an iterable in one expression, with an optional filter.
tags: [python, lists, comprehensions]
---
```python
nums = [1, 2, 3, 4]
[n * n for n in nums]                     # [1, 4, 9, 16]     transform
[n for n in nums if n % 2 == 0]           # [2, 4]            filter: if at the end
["even" if n % 2 == 0 else "odd" for n in nums]   # ['odd', 'even', 'odd', 'even']
[(a, b) for a in "ab" for b in [1, 2]]    # [('a', 1), ('a', 2), ('b', 1), ('b', 2)]
[x for row in [[1, 2], [3]] for x in row] # [1, 2, 3]         flatten
```

- Shape: `[expression for item in iterable if condition]`.
- A filtering `if` goes after the `for`. An `if ... else` that chooses a value goes before the `for`.
- The result is always a new list. The source is not changed.

<!-- more -->

## Details

A comprehension is a short form of a loop that appends:

```python
result = []
for n in nums:
    if n % 2 == 0:
        result.append(n * n)
result                                    # [4, 16]
[n * n for n in nums if n % 2 == 0]       # [4, 16]   the same thing
```

With two `for` clauses, read them left to right as nested loops. The first `for` is the outer loop.

The expression can be anything, including another comprehension. This makes a grid with separate rows:

```python
[[0] * 3 for _ in range(2)]               # [[0, 0, 0], [0, 0, 0]]
```

When you only need to feed the values into a function, drop the brackets. This is a generator expression and it does not build the list in memory:

```python
sum(n * n for n in nums)                  # 30
max(len(w) for w in ["a", "bcd"])         # 3
```

The loop variable lives only inside the comprehension. It does not overwrite a variable of the same name outside.

Keep comprehensions to one transform and one filter. If you need several conditions or a temporary variable, write a normal loop: it is easier to explain aloud.

## Common mistakes

- Putting the filter in the wrong place: `[n if n > 2 for n in nums]` is a `SyntaxError`.
- Reversing the order of two `for` clauses when flattening.
- Using a comprehension only for a side effect such as `print`. Use a loop.
- Forgetting the brackets and getting a generator object instead of a list.

## See also

- [Dict and set comprehensions](#/kb/py-dict-comprehensions)
- [Loops with enumerate, zip and range](#/kb/py-loops-enumerate-zip)
- [lambda, map, filter, any, all](#/kb/py-lambda-map-filter)
- [Iterators and generators](#/kb/py-iterators-generators)
- Official docs: https://docs.python.org/3/tutorial/datastructures.html
