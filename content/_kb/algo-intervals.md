---
title: Merging intervals
summary: Sort intervals by start, then scan once and compare each one with the last one you kept.
tags: [algorithms, sorting, intervals]
---
```python
def merge(intervals):
    out = []
    for start, end in sorted(intervals):       # sort by start
        if out and start <= out[-1][1]:        # overlaps or touches the last
            out[-1][1] = max(out[-1][1], end)  # extend it
        else:
            out.append([start, end])           # gap: start a new one
    return out
merge([[8, 10], [1, 3], [2, 6], [6, 7]])       # [[1, 7], [8, 10]]
```

- "Sort, then scan with the previous item" solves most interval, session and schedule questions.
- The sort costs O(n log n). The scan is O(n).
- Ask whether touching intervals such as `[1, 2]` and `[2, 3]` count as overlapping.

<!-- more -->

## Details

After sorting by start, a new interval can only overlap the **last** interval in the output. So one comparison per item is enough.

Use `max` when you extend. An interval can sit inside the previous one, as `[2, 3]` does inside `[1, 9]`, and then the end must not shrink.

The touching rule is one character. `start <= last_end` merges touching intervals. `start < last_end` keeps them apart.

Two intervals overlap when each one starts before the other ends:

```python
def overlaps(a, b):
    return a[0] <= b[1] and b[0] <= a[1]
overlaps([1, 5], [5, 8])                       # True   (touching counts here)
overlaps([1, 4], [5, 8])                       # False
```

To count how many intervals are open at the same time, turn each interval into two events and sweep:

```python
events = []
for s, e in [[1, 4], [2, 5], [7, 8]]:
    events += [(s, 1), (e, -1)]
live = best = 0
for _, delta in sorted(events):                # at equal times -1 sorts first
    live += delta
    best = max(best, live)
best                                           # 2
```

With this sort order an interval that ends at 4 and one that starts at 4 do not count as overlapping.

Sessions are the same scan: sort the timestamps and start a new group when the gap to the previous one is larger than the limit.

## Common mistakes

- Forgetting to sort. The scan only works on sorted starts.
- Writing `out[-1][1] = end` without `max`, which breaks on nested intervals.
- Passing tuples and then assigning to `out[-1][1]`. Tuples cannot be changed. Append `[start, end]` lists, as the brief does.
- Changing the caller's inner lists. Appending a new `[start, end]` avoids that.
- Not handling empty input. The skeleton returns `[]`, which is usually right.

## See also

- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- [Two pointers](#/kb/algo-two-pointers)
- [Prefix sums and running totals](#/kb/algo-prefix-sums)
