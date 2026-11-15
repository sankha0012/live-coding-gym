**Why this matters.** When a producer is faster than the consumer, an unbounded queue grows until the service runs out of memory. We cap it, decide what to do when it is full, and count what we lose so the loss is never silent.

**How we get there.**
1. Reject bad setup early: a capacity below 1 or an unknown policy raises `ValueError`.
2. Store items in a `collections.deque`. Adding at the back and removing from the front are both constant time, unlike `list.pop(0)`.
3. In `put`, check `len(self._items) >= self.capacity`. If it is full, something is lost, so `self.dropped += 1`.
4. For `"reject"`, return `False` and leave the queue alone. For `"drop_oldest"`, `popleft()` the front item and carry on.
5. Append the new item and return `True`. `get` does `popleft()`, and raises `IndexError` when the queue is empty.

**Check it.** The length never exceeds the capacity. Pushing 100 items into a queue of 5 gives 95 drops under either policy.

**Watch out.** Counting drops under only one policy, or using `list.pop(0)` instead of a deque, are the usual slips.
