`clamp(x, lo, hi)` limits a number to the range from `lo` to `hi`, both included.

- If `x < lo`, it returns `lo`. If `x > hi`, it returns `hi`. Otherwise it returns `x`.
- `lo == hi` is allowed: the result is that value.
- If `lo > hi`, it raises `ValueError`.
- It works with ints and floats, including negative numbers.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import clamp
