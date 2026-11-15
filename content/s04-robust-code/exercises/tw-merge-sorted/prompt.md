`merge_sorted(a, b)` merges two lists of `(key, label)` tuples. Each list is already sorted by key, ascending. Return a new list sorted by key.

- Only the key (first item) is compared, never the label.
- The merge is stable: when a key appears in both lists, the item from `a` comes first. Items within one list keep their order.
- Either list, or both, may be empty.
- The input lists are not modified.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import merge_sorted
