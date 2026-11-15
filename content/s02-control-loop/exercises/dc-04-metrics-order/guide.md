**Why this matters.** scikit-learn takes `(y_true, y_pred)`. A helper that takes the reverse does not fail when you swap them; it quietly reports recall as precision. Only the docs, and a test on lopsided data, reveal it.

**How we get there.**
1. Read `docs.md`: the call is `precision_recall(y_pred, y_true)` and it returns `(precision, recall)`.
2. Our function receives `y_true` first, so flip them: `p, r = precision_recall(y_pred, y_true)`.
3. Compute `f1 = 2 * p * r / (p + r)`, guarding the case `p + r == 0` with `0.0`.
4. Return the three values in a dict.

**Check it.** For `y_true=[1,1,1,0]`, `y_pred=[1,0,0,0]` precision is 1.0 and recall is 1/3. The swapped call would give the opposite.

**Watch out.** F1 is symmetric in precision and recall, so a swap hides there; only the separate precision and recall values reveal it.
