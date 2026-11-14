Write a Python 3.12 function binary_metrics(y_true, y_pred, positive=1) using only the standard library.
- Inputs: two equal-length lists of labels. Output: a dict with the keys "precision", "recall", "f1", each a float, plus the counts "tp", "fp", "fn".
- Count tp, fp and fn for the positive label. precision = tp / (tp + fp), recall = tp / (tp + fn), f1 = 2 * p * r / (p + r).
- Zero division: if a denominator is 0, return 0.0 for that metric. Never raise ZeroDivisionError and never return NaN. This includes f1 when precision and recall are both 0. It happens when there are no predicted positives or no true positives.
- Validate: if the lists have different lengths, raise ValueError. Two empty lists return all zeros.
- Do not use numpy, pandas or sklearn. Do not modify the inputs.
Also write pytest tests for: a normal case with known numbers, perfect predictions, no predicted positives, no true positives, all wrong, empty input and a length mismatch. Check the normal case against a hand calculation. Then explain in a few sentences why accuracy alone is misleading on imbalanced data.
