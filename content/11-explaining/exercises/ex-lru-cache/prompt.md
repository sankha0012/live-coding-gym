Read this listing. It runs on Python 3.12.

```python
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key, default=None):
        if key not in self.data:
            return default
        self.data.move_to_end(key)
        return self.data[key]

    def put(self, key, value):
        if key in self.data:
            self.data.move_to_end(key)
        self.data[key] = value
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)

    def __len__(self):
        return len(self.data)


def cached(cache):
    def wrap(fn):
        def inner(*args):
            hit = cache.get(args)
            if hit is not None:
                return hit
            value = fn(*args)
            cache.put(args, value)
            return value
        return inner
    return wrap


if __name__ == "__main__":
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")
    cache.put("c", 3)
    print(list(cache.data))

    calls = []

    @cached(LRUCache(8))
    def lookup(x):
        calls.append(x)
        return None if x == 0 else x * 10

    lookup(0)
    lookup(0)
    lookup(2)
    lookup(2)
    print(calls)
```

Explain this code as you would to the interviewer after finishing it: what it does, how, complexity, one risk.
