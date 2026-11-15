---
title: "bisect: binary search in a sorted list"
summary: Find where a value sits or belongs in a sorted list in O(log n), and insert while keeping it sorted.
tags: [python, binary search, sorted lists]
---
```python
import bisect
xs = [10, 20, 20, 30]
bisect.bisect_left(xs, 20)     # 1   first index where 20 could go (before equal items)
bisect.bisect_right(xs, 20)    # 3   last index where 20 could go (after equal items)
bisect.bisect_left(xs, 25)     # 3   not present: index where it would be inserted
bisect.bisect_left(xs, 99)     # 4   len(xs), past the end
bisect.insort(xs, 25)          # xs is now [10, 20, 20, 25, 30]
```

- The list must already be sorted. `bisect` does not check.
- The functions return an insertion index, not "found or not found".
- `bisect_left` gives the count of items smaller than x. `bisect_right` gives the count of items smaller than or equal to x.

<!-- more -->

## Details

To test whether a value is present, look at the item at the returned index:

```python
def index_of(xs, x):
    i = bisect.bisect_left(xs, x)
    return i if i < len(xs) and xs[i] == x else -1

index_of([10, 20, 30], 20)     # 1
index_of([10, 20, 30], 25)     # -1
```

The `i < len(xs)` check matters: for a value larger than everything, `i` equals `len(xs)` and `xs[i]` would raise `IndexError`.

Counting with two searches:

```python
xs = [10, 20, 20, 30]
bisect.bisect_right(xs, 20) - bisect.bisect_left(xs, 20)   # 2   how many 20s
len(xs) - bisect.bisect_left(xs, 20)                       # 3   how many items >= 20
```

Mapping a number to a range with a list of cut points:

```python
grades = "FDCBA"
[grades[bisect.bisect([60, 70, 80, 90], s)] for s in [55, 60, 89, 95]]
# ['F', 'D', 'B', 'A']
```

`bisect.bisect` is the same as `bisect_right`. `insort` is the same as `insort_right`.

All functions accept `key=`. The key is applied to the list items, and you pass the already-computed key value to search for:

```python
people = [("ana", 25), ("bo", 31), ("cy", 40)]
bisect.bisect_left(people, 30, key=lambda p: p[1])   # 1
```

Cost: the search is O(log n). `insort` finds the place in O(log n) but the insert itself shifts items, so it is O(n).

## Common mistakes

- Using `bisect` on an unsorted list. It returns a meaningless index with no error.
- Treating the result as "the index of x" without checking `xs[i] == x`.
- Reading `xs[i]` when `i == len(xs)`.
- Mixing up left and right when the list has duplicates.
- Using it on a list sorted in descending order. It assumes ascending.

## See also

- [Binary search](#/kb/algo-binary-search)
- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- [Big-O of common Python operations](#/kb/py-complexity)
- Official docs: https://docs.python.org/3/library/bisect.html
