`top_k(pairs, k)` takes a list of `(name, score)` tuples and returns a new list with the `k` pairs that have the highest score.

- The result is sorted by score, highest first.
- Pairs with equal scores keep the order they had in the input (stable ties).
- If `k` is larger than the list, all pairs are returned. If `k` is 0 or negative, the result is an empty list.
- The input list is never modified.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import top_k
