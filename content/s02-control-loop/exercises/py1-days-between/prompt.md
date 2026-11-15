Write `days_between(a: str, b: str) -> int` that returns the number of days between two dates given as ISO strings `"YYYY-MM-DD"`.

- The result is never negative: the order of `a` and `b` does not matter.
- The same date gives `0`. Leap years count: `"2024-02-28"` to `"2024-03-01"` is `2`.
- If either string is not a valid date (such as `"not-a-date"` or `"2024-02-30"`), raise `ValueError`.
