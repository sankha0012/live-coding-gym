`normalize_scores(values)` rescales a list of numbers to the range 0 to 1 with min-max scaling: `(v - min) / (max - min)`. It returns a new list of floats in the same order.

- The smallest value becomes 0.0 and the largest becomes 1.0.
- If all values are equal (constant input), return a list of 0.0 of the same length. Do not divide by zero.
- An empty list gives an empty list.
- The input list is not modified.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import normalize_scores
