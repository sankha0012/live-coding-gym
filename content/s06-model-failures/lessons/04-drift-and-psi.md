# Drift and PSI

## What it is

Drift means the data the model sees now differs from the data it was trained on. The input features can shift (data drift), or the relationship between features and the label can change (concept drift). The population stability index, PSI, is a common way to measure the first kind: bin a feature or the score, compare the share of rows per bin between a baseline and a new period, and sum a weighted log ratio. See [drift and PSI](#/kb/ml-psi-drift) and [drift alerts](#/kb/prod-drift-alerts-hysteresis).

## How it breaks in production

Nothing crashes. A delivery-time model trained before a holiday season, a new app version that changes how a field is filled, or a new customer segment all move the inputs, and quality erodes slowly. Without monitoring, the first sign is a business metric drop weeks later. A common rule of thumb reads PSI under 0.1 as stable, 0.1 to 0.25 as a moderate shift, and above 0.25 as a large one, but these are conventions, not laws. Another trap is an empty bin: the log of zero is undefined, so you must smooth the proportions.

## The defence in code

Fix the bin edges from the baseline, smooth empty bins, and alarm above a threshold.

```python
import numpy as np

def psi(baseline, current, bins=5, eps=1e-6):
    edges = np.quantile(baseline, np.linspace(0, 1, bins + 1))
    edges[0], edges[-1] = -np.inf, np.inf
    b = np.histogram(baseline, edges)[0] / len(baseline)
    c = np.histogram(current, edges)[0] / len(current)
    b, c = np.clip(b, eps, None), np.clip(c, eps, None)
    return float(np.sum((c - b) * np.log(c / b)))

rng = np.random.default_rng(0)
base = rng.normal(0, 1, 5000)
same = rng.normal(0, 1, 5000)
shifted = rng.normal(1.0, 1, 5000)
assert psi(base, same) < 0.1
assert psi(base, shifted) > 0.25
print(round(psi(base, same), 3), round(psi(base, shifted), 3))
```

The seeded generator keeps the result identical on every run. The bin edges come from the baseline only; recomputing them from the new data would hide the shift. In production you would alarm only after the threshold is crossed for several consecutive windows, to avoid noise.

## What to say in the interview

"To detect drift I would compare the current distribution of each important feature and of the score to a stored baseline using PSI, with bin edges fixed from the baseline and smoothing for empty bins. I would alarm when it stays above about 0.25 for a few windows, and treat that as a prompt to investigate, not an automatic retrain. I know the thresholds are conventions, so I would check them against how much quality actually moved."
