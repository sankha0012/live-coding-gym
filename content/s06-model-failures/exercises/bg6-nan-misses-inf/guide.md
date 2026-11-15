**Why this matters.** A model that overflows or divides by zero returns infinity, not only NaN. If the guard misses it, the infinite score reaches a threshold, a sort or an average and quietly breaks it.

**How we get there.**
1. Run the tests. The ones with infinity fail.
2. Reproduce: `guard_scores([0.2, float('inf'), float('-inf')])`. The result keeps both infinities and reports 0 bad scores.
3. Read the condition. Besides the type checks, the only test on the value itself is `math.isnan`.
4. `inf` is a float and `inf != nan`, so `not math.isnan(inf)` is true and the value counts as good.
5. Replace `not math.isnan(s)` with `math.isfinite(s)`. It is false for NaN, inf and -inf. The `isinstance` check stays first, so strings and bools never reach it.
6. Run the tests again. All pass.

**Check it.** Compare with `solution.py`: the only difference is that one call.

**Next time.** When validating numbers from a model, list NaN, inf, -inf, None, a string and a bool as separate test inputs.

**Watch out.** `math.isfinite("0.4")` raises `TypeError`, so keep the type check before it.
