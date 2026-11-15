---
title: Iterators and generators
summary: Produce values one at a time with yield or a generator expression, and know that they can be read only once.
tags: [python, generators, iteration]
---
```python
def countdown(n):
    while n > 0:
        yield n            # hand out one value, pause here until the next is asked for
        n -= 1

list(countdown(3))         # [3, 2, 1]
g = countdown(2)
next(g)                    # 2
squares = (x * x for x in range(4))   # generator expression: round brackets
sum(squares)               # 14
sum(squares)               # 0   already used up
```

- A function with `yield` returns a generator. Its body runs only when values are requested.
- Generators are lazy: one value at a time, so they use almost no memory.
- An iterator can be consumed once. To loop again, make a new one or store a list.

<!-- more -->

## Details

An iterable is anything you can loop over (list, str, dict, file). An iterator is the object that does the looping: `iter(x)` creates it and `next(it)` gets the next value.

```python
it = iter([1, 2, 3])
next(it)           # 1
next(it)           # 2
list(it)           # [3]   only what is left
next(it, None)     # None  default instead of an error
```

When nothing is left, `next(it)` raises `StopIteration`. A `for` loop catches that for you.

Lists, strings and `range` are reusable because each loop makes a fresh iterator. Generators, `zip`, `map`, `filter`, `enumerate`, open files and `csv.reader` are one-shot.

A typical generator, splitting data into chunks:

```python
def chunks(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]

list(chunks([1, 2, 3, 4, 5], 2))   # [[1, 2], [3, 4], [5]]
```

`yield from other` hands out every value of another iterable:

```python
def numbers():
    yield from [1, 2]
    yield 3

list(numbers())    # [1, 2, 3]
```

Generators work well with `sum`, `min`, `max`, `any`, `all` and `"".join`. `any` stops at the first match, so the rest is never computed:

```python
any(x > 2 for x in countdown(5))   # True
```

Testing membership also consumes values:

```python
g = countdown(3)
2 in g       # True   3 and 2 were used
list(g)      # [1]
```

## Common mistakes

- Looping over a generator twice and getting nothing the second time.
- Calling `len(gen)` or `gen[0]`. Both raise `TypeError`. Convert with `list(gen)` first.
- Calling a generator function and expecting it to run. `countdown(3)` only creates the generator.
- Using `return value` where you meant `yield value`.
- Printing a generator and seeing `<generator object ...>`. Wrap it in `list()`.

## See also

- [itertools: chain, islice, accumulate, groupby, pairwise](#/kb/py-itertools)
- [List comprehensions](#/kb/py-list-comprehensions)
- [Loops with enumerate, zip and range](#/kb/py-loops-enumerate-zip)
- [Chunked batch processing and isolating bad records](#/kb/prod-chunked-batch-processing)
