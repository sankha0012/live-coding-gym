**Why this matters.** Before a new model takes traffic, it can run in shadow: it sees real inputs but its answers are thrown away. We then measure how often it disagrees with the live model. The shadow must never take serving down.

**How we get there.**
1. Loop over the inputs and count `total`. Call `live(x)` first, outside any `try`. If live fails, that is a real incident and it should raise.
2. Wrap only `shadow(x)` in `try/except Exception`. On failure, count a shadow error and `continue`, so that input is neither compared nor a disagreement.
3. Compute `diff = abs(a - b)`. Only when `diff > tolerance` do we store a case dict with the input, both scores and the diff. Exactly at the tolerance is not a disagreement.
4. Sort by `-diff`; the stable sort keeps input order on ties.
5. Return the counts, with `rate = len(cases) / compared` guarded for `compared == 0`, and `worst = cases[:top]`.

**Check it.** The rate divides by inputs actually compared, not by the total.

**Watch out.** Counting shadow errors as disagreements, or dividing by the total, makes a flaky shadow look like a bad model.
