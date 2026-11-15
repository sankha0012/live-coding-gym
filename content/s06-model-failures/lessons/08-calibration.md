# Calibration

## What it is

A model is calibrated when its scores mean what they say: among all cases that received a score near 0.8, about 80 percent are truly positive. Calibration is separate from ranking quality. A model can have an excellent AUC, ordering cases perfectly, and still be badly calibrated, for example by reporting 0.9 for cases that are positive only 60 percent of the time. See [calibration](#/kb/ml-calibration).

## How it breaks in production

Ranking uses only the order, so miscalibration does not hurt it. But any decision that uses the number does: a fixed threshold of 0.5, an expected-cost calculation, a promise shown to a user ("90 percent chance of delivery in time"), or a score combined with another model's score. Training with class weights or resampling, or a model such as a boosted tree or an SVM, commonly shifts the score scale. After a retrain, a threshold that used to give 5 percent flagged traffic may suddenly flag 20 percent, with no error anywhere.

## The defence in code

Check calibration with bins: group scores, then compare the mean score to the observed positive rate in each bin. A large gap means recalibrate, for example with isotonic regression or Platt scaling, fitted on held-out data.

```python
import numpy as np

def calibration_table(y_true, scores, bins=5):
    y_true, scores = np.asarray(y_true), np.asarray(scores)
    ids = np.minimum((scores * bins).astype(int), bins - 1)
    rows = []
    for b in range(bins):
        m = ids == b
        if m.any():
            rows.append((b, int(m.sum()), float(scores[m].mean()), float(y_true[m].mean())))
    return rows

rng = np.random.default_rng(0)
true_p = rng.uniform(0, 1, 5000)
y = (rng.uniform(0, 1, 5000) < true_p).astype(int)

for _, _, mean_score, rate in calibration_table(y, true_p):
    assert abs(mean_score - rate) < 0.05          # calibrated

overconfident = np.sqrt(true_p)  # strictly increasing: same ranking, wrong scale
gaps = [abs(s - r) for _, _, s, r in calibration_table(y, overconfident)]
assert max(gaps) > 0.1
print(round(max(gaps), 2))
```

The overconfident scores are a strictly increasing function of the originals, so they keep the same order and the AUC is unchanged, but the bins expose the gap.

## What to say in the interview

"AUC tells me about ranking, calibration tells me whether the numbers can be trusted as probabilities. If a decision uses a threshold or an expected cost, I check calibration by binning scores and comparing the mean score with the observed positive rate. When the gap is large I recalibrate on held-out data and re-check after each retrain, because the score scale can move even when the ranking does not."
