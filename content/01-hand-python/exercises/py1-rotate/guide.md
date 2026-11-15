**Why this matters.** Rotating a list shows up in round-robin schedules and circular buffers. The real question is what `k` should mean when it is larger than the list or negative.

**How we get there.**
1. An empty list has nothing to rotate, so return `[]` first. This also protects the next step from a division by zero.
2. Reduce `k` with `k %= len(items)`. Rotating by the length changes nothing, so only `k` modulo the length matters, and Python's `%` also maps negative values into the range 0 to length minus 1.
3. Now the last `k` items must move to the front: `items[-k:]` is that tail and `items[:-k]` is the rest.
4. Join them with `+`. Slices make new lists, so the input is never touched.

**Check it.** `k = 0` works: `items[-0:]` is the whole list and `items[:-0]` is empty, so we get a copy back. Time is linear and a new list is built.

**Watch out.** Doing the modulo on an empty list raises `ZeroDivisionError`, and skipping the modulo makes large or negative `k` return wrong slices.
