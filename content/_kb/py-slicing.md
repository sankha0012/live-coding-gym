---
title: Slicing
summary: Take part of a list, string or tuple with seq[start:stop:step], including reversing with [::-1].
tags: [python, lists]
---
```python
xs = [10, 20, 30, 40, 50]
xs[1:3]     # [20, 30]        start included, stop excluded
xs[:2]      # [10, 20]        first two
xs[-2:]     # [40, 50]        last two
xs[::2]     # [10, 30, 50]    every second item
xs[::-1]    # [50, 40, 30, 20, 10]   reversed copy
"hello"[1:4]  # 'ell'         strings slice the same way
```

- A slice never raises `IndexError`: out-of-range bounds are clipped.
- A slice is a new object; the original is not changed.

<!-- more -->

## Details

`seq[start:stop:step]` takes items from index `start` up to but not including `stop`, moving by `step`. Missing parts default to the beginning, the end and 1. Negative indexes count from the end.

Rotating a list by `k` uses two slices:

```python
k = k % len(xs)          # only when xs is not empty
rotated = xs[-k:] + xs[:-k] if k else xs[:]
```

Slice assignment changes a list in place: `xs[1:3] = [0]` replaces two items with one. `xs[:]` makes a shallow copy.

## Common mistakes

- Expecting `xs[-0:]` to mean "the last zero items": `-0` is `0`, so it is the whole list.
- Forgetting that the stop index is excluded.

## See also

- [str.split and str.join](#/kb/py-str-split-join)
- Official docs: https://docs.python.org/3/library/stdtypes.html
