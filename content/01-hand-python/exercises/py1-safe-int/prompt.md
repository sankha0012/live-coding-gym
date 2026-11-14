Write `safe_int(value, default=0)` that converts `value` to an `int` and returns `default` if it cannot.

- `"42"` and `"  7 "` give `42` and `7`. An int stays as it is.
- A float works only if it is a whole number: `7.0` gives `7`, but `7.5` returns `default`. `nan` and `inf` are not whole numbers, so they return `default` too.
- Text that is not an integer returns `default`: `"abc"`, `""` and `"7.0"` (a string with a dot).
- `None` returns `default`.
