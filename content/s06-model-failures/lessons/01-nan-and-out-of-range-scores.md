# NaN and out-of-range scores

## What it is

A model score should be a finite number inside a known range, usually a probability between 0 and 1. In practice a model can return NaN, infinity, None, or a value like 1.3 or -0.2. NaN is the sneakiest: every comparison with it is False, so `nan < 0` and `nan > 1` both fail and a plain range check lets it through. NaN also does not equal itself, so `score == score` is False for it.

## How it breaks in production

NaN usually comes from upstream: a division by zero in a feature, the log of zero, or a missing value that reached the model. Once it is in your data it spreads. A sum that includes one NaN is NaN, a sort with NaN in it gives an order that depends on the algorithm, and a threshold like `score > 0.5` silently treats it as "no". Nobody sees an error. The ranking is just wrong for the affected rows. Out-of-range values are quieter still: a "probability" of 1.3 breaks log-loss and any code that assumes a valid probability. If 20 percent of scores need clipping, the model is broken and the clip is hiding it.

## The defence in code

Check for finiteness first, then range, and count every repair so a silent fix becomes a visible signal. See also [fallbacks](#/kb/prod-fallbacks) and [input validation](#/kb/prod-input-validation).

```python
import math
from collections import Counter

stats = Counter()

def clean_score(score, fallback=0.5):
    if score is None or not isinstance(score, (int, float)) or not math.isfinite(score):
        stats["not_finite"] += 1
        return fallback
    if score < 0.0 or score > 1.0:
        stats["clipped"] += 1
        return min(1.0, max(0.0, score))
    return float(score)

assert clean_score(0.4) == 0.4
assert clean_score(1.3) == 1.0
assert clean_score(-0.2) == 0.0
assert clean_score(float("nan")) == 0.5
assert clean_score(float("inf")) == 0.5
assert clean_score(None) == 0.5
print(dict(stats))
```

The order matters. `min(1.0, max(0.0, nan))` returns 0.0, and swapping the order to `max(0.0, min(1.0, nan))` returns 1.0, with no error either way, so the finite check must come before the clip. The fallback value is a product decision: a neutral 0.5, a rule-based score, or refusing to answer.

## What to say in the interview

"I treat every score as untrusted. I check that it is finite before anything else, because NaN passes every comparison, then I clip small range errors into 0 to 1. Each repair increments a counter, and I would alarm on the rate, since a rising clip rate means the model is broken, not that the clip is working. I would also test the function with NaN, infinity, None and values on both sides of the range."
