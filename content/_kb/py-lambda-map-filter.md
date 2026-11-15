---
title: lambda, map, filter, any, all
summary: Write small one-expression functions with lambda and apply or test them across an iterable.
tags: [python, functions, iteration]
---
```python
nums = [3, -1, 4]
square = lambda x: x * x                 # same as: def square(x): return x * x
list(map(square, nums))                  # [9, 1, 16]    apply to every item
list(filter(lambda x: x > 0, nums))      # [3, 4]        keep items where it is true
any(x < 0 for x in nums)                 # True          at least one
all(x < 0 for x in nums)                 # False         every one
all([]), any([])                         # (True, False) on an empty iterable
list(map(int, "1 2 3".split()))          # [1, 2, 3]
```

- `lambda args: expression` returns the value of its single expression. No statements, no `return`.
- `map` and `filter` return lazy iterators. Wrap them in `list()` to get the values.
- `any` and `all` stop at the first item that decides the answer.

<!-- more -->

## Details

A lambda is most useful as a short `key` or callback argument:

```python
pairs = [("b", 2), ("a", 5)]
sorted(pairs, key=lambda p: p[1], reverse=True)   # [('a', 5), ('b', 2)]
max(pairs, key=lambda p: p[1])                    # ('a', 5)
```

`map` takes any callable, including built-ins and methods. With several iterables it passes one item from each:

```python
list(map(str.upper, ["a", "b"]))                     # ['A', 'B']
list(map(lambda a, b: a + b, [1, 2], [10, 20]))      # [11, 22]
list(filter(None, [0, 1, "", "a", None]))            # [1, 'a']   None keeps truthy items
```

A comprehension does the same job and is often easier to read aloud:

```python
[x * x for x in nums if x > 0]           # [9, 16]
```

`any` and `all` take one iterable of values and test their truthiness. Pass a generator expression so nothing is computed after the answer is known. `all` of an empty iterable is `True`, so guard the empty case when it matters.

```python
words = ["ab", "cd"]
all(w.isalpha() for w in words)          # True
any(len(w) > 2 for w in words)           # False
```

A `map` or `filter` object can be consumed only once. A second loop over it gives nothing.

## Common mistakes

- Printing `map(...)` and seeing `<map object ...>`. Wrap it in `list()`.
- Writing `any(x > 0, nums)`. It needs one iterable: `any(x > 0 for x in nums)`.
- Assuming `all([])` is `False`.
- Naming a long lambda and reusing it. Use `def`: it has a name in error messages.
- Creating lambdas in a loop and expecting each to remember its own loop value. See closures.

## See also

- [List comprehensions](#/kb/py-list-comprehensions)
- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- [Closures and decorators](#/kb/py-closures-decorators)
- [Truthiness, None and "is" versus "=="](#/kb/py-truthiness-none)
- Official docs: https://docs.python.org/3/library/functions.html
