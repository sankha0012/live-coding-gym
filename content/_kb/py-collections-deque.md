---
title: deque and OrderedDict
summary: A deque adds and removes at both ends in O(1). An OrderedDict can move keys to either end.
tags: [python, collections, queues]
---
```python
from collections import deque, OrderedDict
d = deque([1, 2, 3])
d.append(4); d.appendleft(0)   # deque([0, 1, 2, 3, 4])
d.pop()                        # 4    from the right
d.popleft()                    # 0    from the left, O(1)
last = deque(maxlen=3)         # keeps only the newest 3 items
for i in range(5): last.append(i)
list(last)                     # [2, 3, 4]
```

- Use a deque for a queue: `append` to add, `popleft` to take the oldest.
- `deque(maxlen=n)` drops the oldest item automatically when it is full.
- `OrderedDict.move_to_end(key)` and `popitem(last=False)` are the two calls behind an LRU cache.

<!-- more -->

## Details

`list.pop(0)` and `list.insert(0, x)` are O(n) because every other item must shift. A deque does both ends in O(1). The price is that access in the middle, `d[i]`, is slower than a list, and slicing is not supported.

More deque methods:

```python
d = deque([1, 2, 3])
d.rotate(1)            # deque([3, 1, 2])   move items to the right
d.extendleft([8, 9])   # deque([9, 8, 3, 1, 2])   note the reversed order
d[0], d[-1]            # (9, 2)   peek at both ends
```

An empty deque is falsy, so `while queue:` is the usual loop for breadth-first search and other queue work.

`OrderedDict` is a dict with extra methods for reordering:

```python
od = OrderedDict(a=1, b=2, c=3)
od.move_to_end("a")          # order is now b, c, a
od.popitem(last=False)       # ('b', 2)   removes the oldest
od.move_to_end("a", last=False)   # order is now a, c
```

A plain `dict` also keeps insertion order. Use `OrderedDict` when you need `move_to_end` or `popitem(last=False)`. To read the first key of a plain dict use `next(iter(d))`.

One more difference: two `OrderedDict` objects are equal only if the order matches. Plain dicts ignore order when compared.

## Common mistakes

- Using a list as a queue with `pop(0)`. It works but is O(n) per call.
- Calling `popleft()` on an empty deque. It raises `IndexError`.
- Slicing a deque (`d[0:2]`). It raises `TypeError`. Use `list(d)[0:2]` or `itertools.islice`.
- Forgetting that reading a key does not move it in an `OrderedDict`. You must call `move_to_end` yourself.
- Expecting `extendleft` to keep the order of the items you pass.

## See also

- [LRU cache](#/kb/algo-lru-cache)
- [Sliding window](#/kb/algo-sliding-window)
- [Counter and defaultdict](#/kb/py-counter-defaultdict)
- [Big-O of common Python operations](#/kb/py-complexity)
- Official docs: https://docs.python.org/3/library/collections.html
