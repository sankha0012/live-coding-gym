An AI assistant wrote this. The tests fail. Find the bug and fix it with the smallest safe change.

`chunk(items, size)` splits a list into consecutive lists of at most `size` items, in order. The last chunk may be shorter. Every element appears exactly once. An empty list returns `[]`. A `size` below 1 raises `ValueError`. The input is not modified.
