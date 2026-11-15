**Why this matters.** On imbalanced data, F1 is used because it punishes a model that is good on only one of precision or recall. A wrong formula removes that protection without any error.

**How we get there.**
1. Run the tests. The F1 assertions fail, accuracy, precision and recall pass.
2. Reproduce with `y_true = [1, 0, 0, 0]` and `y_pred = [1, 1, 1, 1]`. Precision is 0.25 and recall is 1.0. The function returns F1 = 0.625.
3. By hand the harmonic mean is `2 * 0.25 * 1.0 / 1.25 = 0.4`. So the formula is wrong.
4. Find the F1 line: `(precision + recall) / 2`.
5. Replace it with `2 * precision * recall / (precision + recall) if precision + recall else 0.0`.
6. Run the tests again. All pass.

**Check it.** The harmonic mean is never larger than the arithmetic mean, and equal only when the two are equal. If your F1 is above the plain average, something is off.

**Next time.** When AI code computes a named metric, write down the formula yourself first and compare it line by line.

**Watch out.** Do not forget the zero guard: when both precision and recall are 0.0 the denominator is 0.
