Some exercises are graded by a **metric on unseen data**, not by exact answers. This one is. Use only the standard library.

Write two functions for a one-feature classifier (a "decision stump"):

**`fit_stump(xs, ys)`**

- `xs` is a list of floats, some of which can be `None` (missing). `ys` is a list of 0 or 1 labels of the same length.
- Raise `ValueError` if the lengths differ or if no `x` is present.
- Learn a threshold `t` and a direction `sign` (`1` or `-1`). The stump predicts 1 when `sign * (x - t) > 0`, otherwise 0. Choose the pair that classifies the training rows with a present `x` best.
- Also store a `fallback` prediction for missing inputs: the most common label in `ys` (0 on a tie).
- Return a dict: `{"threshold": t, "sign": sign, "fallback": f}`.
- Fitting the same data twice must give the same model.

**`predict(model, x)`**

Return 0 or 1. If `x` is `None`, return the fallback. Never raise on a missing value.

The hidden tests train on one generated sample and check the accuracy on a larger sample from another seed. The labels contain noise, so 100% is impossible; around 90% is achievable.
