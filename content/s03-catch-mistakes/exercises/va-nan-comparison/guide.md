**Why this matters.** Missing numbers often arrive as `NaN`, and one `NaN` turns a whole sum into `NaN`. We must drop it, but `NaN` is special: it is not equal to anything, itself included.

**How we get there.**
1. Reproduce. `mean_valid([1.0, float("nan"), 3.0])` returns `nan` instead of 2.0, so the filter let the `NaN` through.
2. Locate it: `v != float("nan")` is always true, because `NaN` is unequal to every value. The test can never remove anything.
3. Replace it with `not math.isnan(v)`, which asks the right question.
4. Keep `v is not None` as a separate check, placed first. `math.isnan(None)` raises `TypeError`, and `and` stops before reaching it.
5. Leave the rest: if nothing is left return `None`, otherwise divide by the count.

**Check it.** Zero stays, since we never test truthiness. An empty or all-invalid list gives `None`. One pass, linear time.

**Next time.** Never compare to `NaN` with `==` or `!=`. Test with a `NaN`, a `None`, a zero and an all-invalid list.

**Watch out.** A filter like `if v` removes valid zeros and changes the mean.
