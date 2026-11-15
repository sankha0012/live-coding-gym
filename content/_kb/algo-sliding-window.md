---
title: Sliding window
summary: Keep a running state for a contiguous range and move its edges instead of recomputing every range.
tags: [algorithms, lists, subarrays]
---
```python
def longest_window(xs, k):           # longest run with sum <= k (xs >= 0)
    best = total = left = 0
    for right, x in enumerate(xs):
        total += x                   # grow on the right
        while total > k:             # shrink from the left until valid
            total -= xs[left]
            left += 1
        best = max(best, right - left + 1)
    return best
longest_window([2, 1, 5, 1, 1, 3], 7)   # 3
```

- Use it for "longest, shortest or best contiguous run" questions on lists and strings.
- Each item enters once and leaves once, so it is O(n), not O(n squared).
- The window is `xs[left:right + 1]` and its length is `right - left + 1`.

<!-- more -->

## Details

A window has two edges and a small piece of state that describes what is inside: a sum, a count, a set, a `Counter`. You update the state when an item enters or leaves. You never loop over the inside of the window.

**Variable size** (the brief). Move `right` one step at a time. While the window breaks the rule, move `left`. Record the answer when the window is valid. For "shortest window that reaches a goal", record inside the `while` loop instead.

**Fixed size.** Build the first window, then slide: add the new item and remove the one that fell out.

```python
def max_window_sum(xs, k):           # best sum of k neighbours
    total = sum(xs[:k])
    best = total
    for i in range(k, len(xs)):
        total += xs[i] - xs[i - k]   # one in, one out
        best = max(best, total)
    return best
max_window_sum([2, 1, 5, 1, 1, 3], 3)   # 8
```

For strings the state is often a dictionary of character counts. When a count falls to zero, delete the key, so `len(counts)` stays the number of distinct characters.

For "events within the last k seconds", a `deque` works as the window: append new items on the right and pop expired ones from the left.

## Common mistakes

- Using a shrinking sum window with negative numbers. Shrinking no longer makes the sum smaller, so the logic fails. Use prefix sums there.
- Using `if` where `while` is needed: one new item may force several removals.
- Off-by-one in the length. It is `right - left + 1`.
- Not guarding `k > len(xs)` or `k <= 0` in the fixed-size version.
- Calling `sum(xs[left:right + 1])` inside the loop, which brings back O(n squared).

## See also

- [Two pointers](#/kb/algo-two-pointers)
- [Prefix sums and running totals](#/kb/algo-prefix-sums)
- [deque and OrderedDict](#/kb/py-collections-deque)
