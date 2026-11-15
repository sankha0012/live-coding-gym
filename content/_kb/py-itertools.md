---
title: "itertools: chain, islice, accumulate, groupby, pairwise"
summary: Ready-made loops for joining, cutting, running totals, grouping neighbours and pairing items.
tags: [python, itertools, iteration]
---
```python
from itertools import chain, islice, accumulate, groupby, pairwise
list(chain([1, 2], [3], [4, 5]))        # [1, 2, 3, 4, 5]     join iterables
list(islice("abcdef", 1, 4))            # ['b', 'c', 'd']     slice any iterable
list(accumulate([1, 2, 3, 4]))          # [1, 3, 6, 10]       running total
list(pairwise([1, 4, 9, 16]))           # [(1, 4), (4, 9), (9, 16)]   neighbours
[(k, len(list(g))) for k, g in groupby("aabaa")]   # [('a', 2), ('b', 1), ('a', 2)]
```

- Every function returns a lazy iterator. Wrap it in `list()` to see the values.
- `groupby` only groups items that are next to each other. Sort by the same key first for full groups.
- An iterator can be read once. After that it is empty.

<!-- more -->

## Details

`chain.from_iterable` flattens one level of nesting:

```python
list(chain.from_iterable([[1, 2], [3]]))   # [1, 2, 3]
```

`islice(it, stop)` or `islice(it, start, stop, step)` works like a slice but on any iterable, including endless ones. It does not accept negative numbers.

```python
from itertools import count
list(islice(count(10), 3))                 # [10, 11, 12]
```

`accumulate` takes an optional function and an optional starting value:

```python
list(accumulate([3, 1, 4, 1], max))        # [3, 3, 4, 4]   running maximum
list(accumulate([1, 2, 3], initial=0))     # [0, 1, 3, 6]
```

`pairwise` is the clean way to compare each item with the next one:

```python
[b - a for a, b in pairwise([1, 4, 9, 16])]   # [3, 5, 7]
```

`groupby(items, key=...)` yields `(key, group)` pairs. Each group is itself an iterator, so turn it into a list at once:

```python
words = ["apple", "avocado", "banana", "cherry"]
{k: list(g) for k, g in groupby(words, key=lambda w: w[0])}
# {'a': ['apple', 'avocado'], 'b': ['banana'], 'c': ['cherry']}
```

Other useful ones:

```python
from itertools import combinations, permutations, product, zip_longest, batched
list(combinations("abc", 2))     # [('a', 'b'), ('a', 'c'), ('b', 'c')]
list(permutations([1, 2, 3], 2)) # [(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)]
list(product("ab", [1, 2]))      # [('a', 1), ('a', 2), ('b', 1), ('b', 2)]
list(zip_longest([1, 2, 3], "ab", fillvalue="-"))   # [(1, 'a'), (2, 'b'), (3, '-')]
list(batched(range(7), 3))       # [(0, 1, 2), (3, 4, 5), (6,)]   Python 3.12+
```

## Common mistakes

- Using `groupby` on unsorted data and getting the same key several times.
- Printing the iterator itself and seeing `<itertools.chain object ...>` instead of values.
- Keeping a `groupby` group for later. It is empty once the loop moves to the next key.
- Expecting `pairwise` on a one-item list to give something. It gives nothing.

## See also

- [Iterators and generators](#/kb/py-iterators-generators)
- [Loops with enumerate, zip and range](#/kb/py-loops-enumerate-zip)
- [Prefix sums and running totals](#/kb/algo-prefix-sums)
- Official docs: https://docs.python.org/3/library/itertools.html
