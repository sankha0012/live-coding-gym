---
title: Two pointers
summary: Walk two indexes over a sequence, usually a sorted one, to replace a nested loop with one pass.
tags: [algorithms, lists, sorted]
---
```python
def pair_with_sum(xs, target):       # xs must be sorted
    lo, hi = 0, len(xs) - 1
    while lo < hi:
        total = xs[lo] + xs[hi]
        if total == target:
            return lo, hi
        if total < target:
            lo += 1                  # need a bigger sum
        else:
            hi -= 1                  # need a smaller sum
    return None
pair_with_sum([1, 3, 4, 6, 9], 10)   # (0, 4)
```

- Use it when the input is sorted (or can be sorted) and you look for a pair, or compare both ends.
- Each step moves one pointer, so the scan is O(n) time and O(1) extra space.
- If you must sort first, the total is O(n log n).

<!-- more -->

## Details

There are two shapes.

**Opposite ends.** `lo` starts at the left and `hi` at the right, and they move toward each other. The loop is `while lo < hi`. This fits pair sums in sorted data, reversing in place and palindrome checks:

```python
def is_palindrome(s):
    lo, hi = 0, len(s) - 1
    while lo < hi:
        if s[lo] != s[hi]:
            return False
        lo, hi = lo + 1, hi - 1
    return True
is_palindrome("level")               # True
```

**Same direction.** A `read` pointer visits every item and a `write` pointer marks where the next kept item goes. This filters or de-duplicates a list in place:

```python
def dedupe_sorted(xs):               # returns the new length
    write = 0
    for read in range(len(xs)):
        if write == 0 or xs[read] != xs[write - 1]:
            xs[write] = xs[read]
            write += 1
    return write
xs = [1, 1, 2, 2, 2, 5]
n = dedupe_sorted(xs)
xs[:n]                               # [1, 2, 5]
```

The same idea merges two sorted lists: one pointer per list, take the smaller item, advance that pointer.

The pattern works because sorted order tells you which pointer to move. If the sum is too small, only moving `lo` right can help.

## Common mistakes

- Using opposite-end pointers on unsorted data. Sort first, or use a dictionary lookup.
- Writing `while lo <= hi` for pairs, which lets one item pair with itself.
- Forgetting to move a pointer in one branch, which gives an infinite loop.
- Sorting when the task asks for original indexes. Sorting loses them unless you keep `(value, index)` pairs.

## See also

- [Sliding window](#/kb/algo-sliding-window)
- [Binary search](#/kb/algo-binary-search)
- [Hash map counting and lookup](#/kb/algo-hash-map-counting)
- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
