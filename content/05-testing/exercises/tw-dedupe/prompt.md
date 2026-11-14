`dedupe(items)` removes duplicates from a list and returns a new list.

- Items are hashable (ints, strings, tuples).
- The first occurrence of each item is kept, and the original order is preserved: `dedupe([3, 1, 2, 3, 1])` is `[3, 1, 2]`.
- The input list is never modified, and the result is a different list object.
- An empty list returns an empty list. A list without duplicates comes back equal.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import dedupe
