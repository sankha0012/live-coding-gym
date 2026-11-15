**Why this matters.** A model can return `NaN`, infinity or `None` instead of a score, and one bad value can poison an average or a ranking downstream. We replace them and count how often it happens.

**How we get there.**
1. Build a new `clean` list and a counter. The input list is never touched.
2. First check the type: `isinstance(s, (int, float))`. We must do this before the math, because `math.isfinite` raises on a string or `None`.
3. Exclude bools explicitly. `True` is an `int` in Python, so without `not isinstance(s, bool)` it would pass as the score 1.
4. Then use `math.isfinite(s)`, which is false for `NaN`, `inf` and `-inf`. `NaN` never equals itself, so an equality check cannot catch it, but this one call handles all three.
5. A good score is appended as it is. Otherwise append `fallback` and add one to the bad count. Order and length are preserved.

**Check it.** An empty list returns `([], 0)`. Time and space are linear.

**Watch out.** Checking only for `NaN` lets infinities through, and writing into the input list changes data the caller still owns.
