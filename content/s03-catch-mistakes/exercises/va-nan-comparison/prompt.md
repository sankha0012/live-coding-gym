An AI assistant wrote this. The tests fail. Find the bug and fix it with the smallest safe change.

`mean_valid(values)` returns the mean of the numbers in `values`, ignoring `None` and `NaN`. Zero is a valid value and must be counted. If nothing valid is left (including an empty list), it returns `None`.
