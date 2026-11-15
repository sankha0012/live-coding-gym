With 1% fraud, a model that always says "not fraud" is 99% accurate and useless. Write `binary_metrics(y_true: list[int], y_pred: list[int]) -> dict` for labels 0 and 1, where 1 is the positive class.

Return a dict with the keys `accuracy`, `precision`, `recall` and `f1` (floats). Precision is TP / (TP + FP), recall is TP / (TP + FN), and f1 is the harmonic mean of the two, 2PR / (P + R). When a denominator is zero, that metric is 0.0 (no crash). Empty lists return all four as 0.0. If the lists have different lengths, raise `ValueError`.


An AI assistant wrote the code below. The tests fail. Find the bug, fix it by hand, then name it in one sentence.
