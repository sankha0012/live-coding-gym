**Why this matters.** With 1% fraud, a model that always says "not fraud" is 99% accurate and catches nothing. Precision, recall and F1 expose that, but their formulas divide by counts that can be zero.

**How we get there.**
1. Check the lengths first and raise `ValueError` if they differ.
2. Count true positives, false positives and false negatives from the pairs, plus how many predictions were correct.
3. Precision is `tp / (tp + fp)`: of what we flagged, how much was right. Recall is `tp / (tp + fn)`: of the real positives, how many we found. Write each as `a / b if b else 0.0`, so a model that never predicts positive gives 0.0 instead of a crash.
4. F1 is the harmonic mean, `2 * p * r / (p + r)`, guarded the same way.
5. Accuracy is `correct / n`, guarded for empty input, so empty lists give four zeros.

**Check it.** Cost is linear. The always-negative model has high accuracy and recall 0.0.

**Watch out.** `(p + r) / 2` is not F1, since the harmonic mean punishes a weak side harder. Swapping precision and recall is the other trap.
