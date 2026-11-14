# Catalog of model failures

## The problem it solves

A model in production rarely fails with a loud crash. It fails quietly: a score of NaN, a feature that is always zero, a model that is three weeks old. Nobody sees an error, but the business numbers slide. In a live-coding round you are often given a small scoring function and asked what could go wrong. This lesson is the list you check, out loud, in the same order each time.

For each failure you need four things: the symptom (what you see), the cause (why it happens), the detection (how you notice) and the defence (what the code does about it).

## The catalog

| Failure | Symptom | Cause | Detection | Defence |
|---|---|---|---|---|
| NaN or inf score | Sorting breaks, sums become NaN | Division by zero, log of 0, bad input | `math.isfinite` | Reject, then fall back |
| Out-of-range score | Probability of 1.3 or -0.2 | Bad post-processing, wrong head | Range check | Clip, and count the clips |
| Missing feature | KeyError, or None in arithmetic | Upstream job late or renamed column | Null rate per feature | Default value plus a flag |
| Stale model | Old behaviour, falling quality | Retrain job failed silently | Model age greater than limit | Alarm, then fall back |
| Stale data | Right model, wrong inputs | Feed stopped updating | Newest timestamp age | Alarm, refuse to serve |
| Label leakage | Perfect offline score, poor live score | A feature is built from the answer | Feature almost equals label | Drop the feature |
| Class imbalance | 99 percent accuracy, useless model | Rare positive class | Precision and recall | Report both, not accuracy |
| Miscalibration | Score 0.9 but only 60 percent are positive | Training changed the score scale | Calibration bins | Recalibrate |
| Drift | Slow quality loss | Inputs change over time | PSI or mean shift | Alarm on a threshold |
| Duplicate events | Counts too high | At-least-once delivery | Repeated event ids | Dedupe by id |
| Train-serve skew | Good offline, bad online | Different code builds features | Compare feature values | One shared function |
| Timezone bug | Off by hours near midnight | Naive datetimes mixed with UTC | Test around midnight | Use UTC everywhere |
| Off-by-one window | Metric slightly wrong | Inclusive versus exclusive edge | Test the boundary | State the rule, test it |
| Partial batch failure | One bad row kills the job | No per-row isolation | Error count | try/except per row |

## The smallest runnable example

This function checks one score for the first three problems in the table: missing, NaN or inf, and out of range.

```python
import math


def check_score(score, limit=(0.0, 1.0)):
    """Return (clean_score, problem). problem is None when all is well."""
    if score is None:
        return None, "missing"
    if not isinstance(score, (int, float)) or not math.isfinite(score):
        return None, "not_finite"
    lo, hi = limit
    if score < lo or score > hi:
        return min(hi, max(lo, score)), "clipped"
    return float(score), None


assert check_score(0.4) == (0.4, None)
assert check_score(1.3) == (1.0, "clipped")
assert check_score(float("nan")) == (None, "not_finite")
assert check_score(None) == (None, "missing")
print("ok")
```

Notice that the function returns the problem as well as the value. A silent fix is a hidden bug. If you clip, you must also count the clips, or you will never know the model is producing bad numbers.

## Three traps people hit

1. **Fixing without counting.** Clipping 1.3 to 1.0 looks safe. But if 20 percent of scores need clipping, the model is broken and the clip hides it. Every repair needs a counter.
2. **Trusting accuracy.** With 1 percent positives, a model that always says "negative" scores 99 percent accuracy. It finds no positives at all. Always ask for precision and recall.
3. **Treating NaN like a number.** `nan < 0` and `nan > 1` are both False, so a range check alone lets NaN pass. Test `math.isfinite` first. Also, `nan == nan` is False, so you cannot detect it with equality.

A fourth, smaller trap: a perfect offline score is a warning, not a win. If a validation score is 0.99 on a hard problem, look for leakage before you celebrate.

## Say it like this

"Before I call this done, I will go through the failure modes. Scores can be NaN or out of range, so I check them and fall back. Features can be missing, so I use a default and count it. The model or the data can be stale, so I check their age. For quality I would not use accuracy alone, because of class imbalance. I would also watch drift and duplicates. For each repair I keep a counter, so a silent problem becomes a visible one."
