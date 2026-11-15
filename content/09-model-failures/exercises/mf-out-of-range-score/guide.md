**Why this matters.** A post-processing bug can push probabilities below 0 or above 1. We still return a usable answer, but we also report how often it happened, because a growing count points to an upstream bug.

**How we get there.**
1. Clip one value with `min(max(p, 0.0), 1.0)`. `max` lifts anything below 0 up to 0.0, and `min` pulls anything above 1 down to 1.0.
2. Apply that with a list comprehension. It builds a new list, so the input is untouched and the length and order are kept.
3. Count the changed values separately with `p < 0.0 or p > 1.0`, using the original values. After clipping, everything looks valid.
4. Return both, so the caller gets safe numbers and a count to alert on.

**Check it.** Exactly 0 and exactly 1 are valid, so the comparisons are strict. An empty list gives `([], 0)`. Time and space are linear.

**Watch out.** `<=` and `>=` raise false alarms on valid boundary scores, and dropping out-of-range rows breaks the one-answer-per-row shape.
