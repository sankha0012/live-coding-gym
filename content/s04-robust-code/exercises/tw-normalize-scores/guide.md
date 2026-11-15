**Why this matters.** Min-max scaling is one formula, but real data breaks it: constant columns, single values and empty lists all make the division or the `min` fail. Tests must visit those inputs.

**How we get there.**
1. Test a normal case where the minimum is not zero, `[10, 20, 30]` giving `0.0, 0.5, 1.0`. Dividing by the max alone would give the wrong answer here.
2. Add negatives and a shuffled order, `[5, -5, 0]`, to check the formula and that order is kept.
3. Test constant input, `[7, 7, 7]`. The range is zero, and the spec wants zeros, not a `ZeroDivisionError`. A single value, `[3]`, is the same case.
4. Test the empty list. `min([])` raises, so the function needs its own early return.
5. Check the input is unchanged. In-place rescaling would corrupt the raw data for later steps.

**Check it.** Use `pytest.approx` for floats. The correct version scans the list a few times, so it is linear in length.

**Watch out.** If every test input starts at zero or has distinct values, the wrong formula and the division by zero both go unnoticed.
