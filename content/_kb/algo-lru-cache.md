---
title: LRU cache
summary: A size-limited cache that evicts the least recently used key, built on an ordered dict.
tags: [algorithms, caching, dicts]
---
```python
from collections import OrderedDict
d = OrderedDict(a=1, b=2, c=3)     # oldest first
d.move_to_end("a")                 # "a" was just used, so it is the newest
list(d)                            # ['b', 'c', 'a']
d["d"] = 4                         # new keys go to the end
d.popitem(last=False)              # ('b', 2)   evict the least recently used
list(d)                            # ['c', 'a', 'd']

from functools import lru_cache
@lru_cache(maxsize=128)            # ready-made LRU for function results
def square(n): return n * n
```

- LRU means: when the cache is full, drop the key that was read or written longest ago.
- With an ordered dict, `get` and `put` are both O(1).
- To cache a pure function, use `functools.lru_cache` and do not write a class.

<!-- more -->

## Details

Keep the keys ordered from least recent (front) to most recent (end). The two operations are:

- **get(key)**: if the key is missing, return the default. Otherwise move it to the end and return its value. A read counts as a use.
- **put(key, value)**: store the value, move the key to the end, and if the size is now above the capacity, pop the item at the front.

A plain `dict` also keeps insertion order, so it can do the same job. Reinsert a key to make it the newest:

```python
d = {"a": 1, "b": 2}
d["a"] = d.pop("a")                # reinsert: "a" is now last
next(iter(d))                      # 'b'   the oldest key
del d[next(iter(d))]               # evict it
d                                  # {'a': 1}
```

`lru_cache` wraps a function and keys the cache on its arguments, which must be hashable:

```python
square(3); square(3)
square.cache_info()   # CacheInfo(hits=1, misses=1, maxsize=128, currsize=1)
square.cache_clear()
```

In an interview, say why a dict alone is not enough: it finds a key in O(1), but you also need the usage order. The classic design is a dict plus a doubly linked list. `OrderedDict` is exactly that.

## Common mistakes

- Not moving the key on `get`. Then the cache evicts by insertion order (FIFO), not by use.
- Updating an existing key without moving it to the end. Assigning to an existing key keeps its old position.
- Evicting before the insert and so dropping a key when only an update happened. Insert first, then check `len(d) > capacity`.
- Calling `popitem()` with no argument. It removes the newest item. Use `last=False`.
- Using `lru_cache` on a function that takes a list or dict, which raises `TypeError: unhashable type`.

## See also

- [deque and OrderedDict](#/kb/py-collections-deque)
- [Caches with a TTL](#/kb/prod-ttl-cache)
- [Closures and decorators](#/kb/py-closures-decorators)
- [Dictionaries: get, setdefault, items, membership](#/kb/py-dicts)
