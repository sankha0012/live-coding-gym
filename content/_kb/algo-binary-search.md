---
title: Binary search
summary: Halve a sorted range at every step to find a value or a boundary in O(log n).
tags: [algorithms, sorted, search]
---
```python
def search(xs, target):        # xs sorted; returns an index or -1
    lo, hi = 0, len(xs) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if xs[mid] == target:
            return mid
        if xs[mid] < target:
            lo = mid + 1       # target is to the right
        else:
            hi = mid - 1       # target is to the left
    return -1
search([1, 3, 5, 8], 5)        # 2
```

- The data must be sorted, or the question must be "false, false, true, true" along a range.
- O(log n) time, O(1) space. One million items need about 20 steps.
- For "where would it go" questions, use the `bisect` module instead of writing the loop.

<!-- more -->

## Details

Two templates cover almost everything.

**Exact match** (the brief). Both ends are included, the loop is `while lo <= hi`, and both updates skip `mid` with `+ 1` and `- 1`.

**First position where a condition becomes true.** The condition must be false for a while and then true for the rest. The loop is `while lo < hi`, and a true `mid` is kept because it may be the answer:

```python
def first_true(lo, hi, ok):    # smallest n in [lo, hi] with ok(n)
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid           # keep mid
        else:
            lo = mid + 1
    return lo
first_true(0, 100, lambda n: n * n >= 50)   # 8
```

This also searches over answers, not only lists: "the smallest capacity that is enough", "the first bad version". It assumes `ok(hi)` is true.

`bisect` gives insertion points in a sorted list:

```python
import bisect
xs = [1, 3, 3, 8]
bisect.bisect_left(xs, 3)      # 1   first index with xs[i] >= 3
bisect.bisect_right(xs, 3)     # 3   first index with xs[i] > 3
bisect.bisect_left(xs, 4)      # 3   not found: where it would go
```

`bisect_right - bisect_left` is the number of copies of a value.

## Common mistakes

- Searching unsorted data. The result is wrong and there is no error.
- Mixing templates: `while lo <= hi` with `hi = mid` loops forever.
- Forgetting `+ 1` in `lo = mid + 1`, which also loops forever when `lo` and `hi` are neighbours.
- Treating a `bisect_left` result as "found". Check `i < len(xs) and xs[i] == target`.
- Expecting the first copy among duplicates. The exact-match template returns any copy.

## See also

- [bisect: binary search in a sorted list](#/kb/py-bisect)
- [Two pointers](#/kb/algo-two-pointers)
- [Big-O of common Python operations](#/kb/py-complexity)
