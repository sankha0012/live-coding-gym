**Why this matters.** A fraud model gives a score, and someone must pick the cut-off that turns it into yes or no. Accuracy hides missed fraud when positives are rare, so we measure precision and recall at that threshold.

**How we get there.**
1. Walk labels and scores together with `zip`, and predict `1 if pi >= t else 0`.
2. In the same loop count true positives, false positives (predicted 1, actually 0) and false negatives (predicted 0, actually 1).
3. Precision is `tp / (tp + fp)`: of the cases we flagged, how many were real. Recall is `tp / (tp + fn)`: of the real cases, how many we caught.
4. F1 is `2 * prec * rec / (prec + rec)`, low whenever either side is low.
5. Each division can have a zero denominator, so each gets its own guard: `... if denominator else 0.0`.

**Check it.** A batch with no positives and no flags has zero denominators everywhere and returns `(0.0, 0.0, 0.0)`. One pass, so linear time and constant space.

**Watch out.** Guarding only precision is the usual slip: recall or F1 can still divide by zero.
