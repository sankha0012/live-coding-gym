Write a class `BoundedQueue(capacity: int, policy: str = "drop_oldest")` that sits between a fast producer and a slow consumer.

- `put(item) -> bool` adds an item at the back and returns `True` if the item was accepted, `False` if it was refused.
- `get()` removes and returns the item at the front (first in, first out). If the queue is empty it raises `IndexError`.
- `len(q)` is the number of items now in the queue. It never goes above `capacity`.
- When the queue is full:
  - policy `"drop_oldest"`: remove the oldest item, add the new one, return `True`. The removed item counts as dropped.
  - policy `"reject"`: keep the queue as it is, refuse the new item, return `False`. The refused item counts as dropped.
- The attribute `dropped` is the total number of items dropped so far (starts at 0).
- Raise `ValueError` if `capacity` is less than 1 or the policy is not one of the two names.
