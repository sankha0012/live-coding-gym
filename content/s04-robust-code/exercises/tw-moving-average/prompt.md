# Test `moving_average`

`moving_average(values, window)` returns the mean of every run of `window` consecutive numbers.

- The result has `len(values) - window + 1` items, one per window, in order. Example: `moving_average([1, 2, 3, 4], 2)` is `[1.5, 2.5, 3.5]`.
- If `window` is larger than the list (or the list is empty), it returns `[]`.
- If `window` is less than 1, it raises `ValueError`.
- It never changes the list it is given.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import moving_average
