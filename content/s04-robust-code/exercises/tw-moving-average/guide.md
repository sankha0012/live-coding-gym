**Why this matters.** Moving averages are full of off-by-one traps: how many windows are there, and what happens when the window does not fit? The tests have to count carefully.

**How we get there.**
1. Test a small list you can compute by hand, `[1, 2, 3, 4]` with window 2 giving `[1.5, 2.5, 3.5]`. Three windows come from `len - window + 1`, so a version that stops one early misses the last item.
2. Test window equal to the length. It gives exactly one mean, which also exposes the off-by-one.
3. Test a window larger than the list, and an empty list. Both must give `[]`, not a mean of whatever is there.
4. Test windows below 1 with `pytest.raises(ValueError)`, for both `0` and `-1`. A version that quietly returns `[]` instead of raising fails.
5. Use unsorted input and compare it afterwards. A version that sorts the list in place changes both the averages and the caller's data.

**Check it.** The correct version sums each slice, so it costs time proportional to `len * window`.

**Watch out.** Tests that only try the happy path pass every buggy version. The edge tests do the real work.
