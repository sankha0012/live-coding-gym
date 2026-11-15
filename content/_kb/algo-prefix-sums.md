---
title: Prefix sums and running totals
summary: Precompute cumulative sums once, then get the sum of any range with one subtraction.
tags: [algorithms, lists, itertools]
---
```python
from itertools import accumulate
xs = [3, 1, 4, 1, 5]
prefix = [0] + list(accumulate(xs))   # [0, 3, 4, 8, 9, 14]
prefix[4] - prefix[1]                 # 6    sum of xs[1:4], in O(1)

total, running = 0, []
for x in xs:                          # the same running total by hand
    total += x
    running.append(total)
running                               # [3, 4, 8, 9, 14]
```

- `prefix[i]` is the sum of the first `i` items, so `sum(xs[i:j]) == prefix[j] - prefix[i]`.
- Building costs O(n) once. Every range sum after that is O(1).
- Use it for many range queries, running balances and cumulative metrics.

<!-- more -->

## Details

The leading `0` matters. It makes `prefix` one item longer than `xs`, so the indexes match slice bounds and a range that starts at 0 needs no special case.

`accumulate` takes any two-argument function, so the same tool gives a running maximum or minimum:

```python
list(accumulate(xs, max))             # [3, 3, 4, 4, 5]   running maximum
deltas = [50, -30, -40, 60]
min(accumulate(deltas))               # -20   the balance went below zero
```

A running average needs the running total and the position:

```python
[round(t / i, 2) for i, t in enumerate(accumulate(xs), start=1)]
# [3.0, 2.0, 2.67, 2.25, 2.8]
```

**Prefix sums plus a dictionary.** A range `xs[i:j]` has sum `k` exactly when `prefix[j] - prefix[i] == k`. So while you scan, store each prefix value you have seen in a dict, and ask whether `current - k` is already there. This answers "is there a contiguous run with sum k" in O(n), and it works with negative numbers, where a sliding window does not.

In a grid the same idea works per row or in two dimensions. In pandas the running total is `cumsum()`.

## Common mistakes

- Leaving out the leading `0` and then being off by one on every range.
- Mixing inclusive and exclusive ends. With the leading zero, `prefix[j] - prefix[i]` covers `xs[i:j]`, and `j` is excluded.
- Calling `sum(xs[i:j])` inside a loop over many ranges. That is O(n) per query.
- Reusing the `accumulate` object. It is an iterator and is empty after one pass. Wrap it in `list(...)`.
- Summing floats and comparing with `==`. Rounding errors add up, so compare with a tolerance.

## See also

- [itertools: chain, islice, accumulate, groupby, pairwise](#/kb/py-itertools)
- [Sliding window](#/kb/algo-sliding-window)
- [Hash map counting and lookup](#/kb/algo-hash-map-counting)
