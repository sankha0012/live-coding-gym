**Why this matters.** Real input is messy: strings from forms, `None` from missing fields, floats from files. We want a number or a safe fallback, never a crash, and never a silently wrong number.

**How we get there.**
1. Start with the conversion `int(value)` inside a `try`. It handles `"42"`, `"  7 "` and ints.
2. Bad text such as `"abc"`, `""` or `"7.0"` raises `ValueError`, and `None` raises `TypeError`. Catch exactly those two and return `default`.
3. Floats need their own branch before the conversion, because `int(7.5)` does not fail: it quietly cuts off to `7`.
4. For a float, accept it only if `value.is_integer()`, otherwise return `default`. `nan` and `inf` are not whole numbers, so they fall to `default` as well.

**Check it.** Each call is constant time.

**Watch out.** Trusting `int()` on floats loses data without any error, and a bare `except:` would swallow real bugs along with the expected ones.
