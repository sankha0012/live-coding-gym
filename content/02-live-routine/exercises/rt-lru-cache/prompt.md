Write a class `LRUCache(capacity)` with two methods. `get(key)` returns the value, or `-1` if the key is missing. `put(key, value)` stores the pair. A `get` or a `put` on a key makes it the most recently used. When a `put` of a new key would go over `capacity`, remove the least recently used key first. Putting an existing key updates its value and does not evict anything. `capacity` is at least 1. Both methods should run in O(1).

Example with capacity 2: `put(1, 1)`, `put(2, 2)`, `get(1)` returns `1`, `put(3, 3)` evicts key 2, so `get(2)` returns `-1`.
