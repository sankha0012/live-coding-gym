---
title: Big-O of common Python operations
summary: How the cost of list, dict, set, deque, heap and sort operations grows with the size of the data.
tags: [python, complexity, performance]
---
```python
x in some_list        # O(n)        scans every item
x in some_set         # O(1)        hash lookup (same for dict keys)
d[key] = value        # O(1)
xs.append(x)          # O(1)        xs.pop() too
xs.insert(0, x)       # O(n)        xs.pop(0) too: everything shifts
sorted(xs)            # O(n log n)
min(xs), sum(xs)      # O(n)
```

- Big-O says how the work grows when the input grows. Constant factors are ignored.
- Membership tests in a loop: use a `set` or `dict`, not a `list`.
- A loop inside a loop over the same data is O(n²). Look for a dict or set to remove the inner loop.

<!-- more -->

## Details

From fastest to slowest growth: O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n), O(n²) quadratic, O(2ⁿ) exponential. For a million items, O(n) is a million steps and O(n²) is a million million.

```
list    xs[i], append, pop(), len            O(1)
        x in xs, index, count, remove        O(n)
        insert(0, x), pop(0), del xs[i]      O(n)
        xs[a:b], xs.copy(), reversed copy    O(k)   k = items copied
        sort, sorted                         O(n log n)
dict    d[k], k in d, get, d[k] = v, del     O(1) on average
set     x in s, add, remove                  O(1) on average
        a | b, a & b                         O(len(a) + len(b)) roughly
deque   append, appendleft, pop, popleft     O(1)
        d[i] in the middle                   O(n)
heapq   heappush, heappop                    O(log n)
        heapify                              O(n)       h[0] is O(1)
bisect  bisect_left, bisect_right            O(log n)   insort is O(n)
str     s + t, s[a:b], "".join(parts)        O(length of the result)
        sub in s                             O(n) in normal cases
```

`len()` is O(1) for every built-in container.

Hidden costs to watch for:

- `x in xs` inside a `for` loop makes the whole thing O(n²).
- `s += piece` in a loop copies the string each time. Collect pieces in a list and `"".join` once.
- Slicing copies. `xs[1:]` in every loop turn is O(n) each time.

The classic improvement, from O(n²) pairs to O(n) with a set:

```python
def has_duplicate(xs):
    seen = set()
    for x in xs:
        if x in seen:          # O(1)
            return True
        seen.add(x)
    return False
```

Space counts too: the set costs O(n) extra memory. To state a complexity, say what `n` is, then the time, then the extra space.

## Common mistakes

- Using a list for lookups in a loop instead of a set or dict.
- Calling `pop(0)` or `insert(0, x)` repeatedly. Use `collections.deque`.
- Sorting inside a loop when one sort before the loop is enough.
- Quoting only time complexity and forgetting the extra space.

## See also

- [deque and OrderedDict](#/kb/py-collections-deque)
- [Sets and set operations](#/kb/py-sets)
- [Hash map counting and lookup](#/kb/algo-hash-map-counting)
- [Explaining code: structure and phrases](#/kb/iv-explaining-code)
