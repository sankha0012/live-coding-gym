# Missing features and fallbacks

## What it is

At serving time the model receives a row of features built from other systems. Some of those features will be absent: the upstream job was late, a column was renamed, a user is new and has no history. A missing feature shows up as a KeyError, a None, or a NaN. A fallback is the planned answer for when the model cannot do its job.

## How it breaks in production

If the code does `row["orders_30d"]` and the key is gone, one request raises and a whole batch may die. If the value is None, the arithmetic fails somewhere deeper, with an error far from the cause. Worse is the silent version: a pipeline fills missing values with 0, which looks like a real value. The model then treats new users as customers with zero orders, and nobody can tell the difference between "zero" and "unknown". A null rate that jumps from 1 to 40 percent can degrade the model for days without an exception.

## The defence in code

Use an explicit default, a missing flag, and a counter. If the model itself fails, fall back to a simple rule, then to a constant that cannot raise. See [fallbacks](#/kb/prod-fallbacks) and [missing values](#/kb/pd-missing-values).

```python
import math
from collections import Counter

stats = Counter()

def get_feature(row, name, default=0.0):
    value = row.get(name)
    if value is None or (isinstance(value, float) and math.isnan(value)):
        stats["missing_" + name] += 1
        return default, 1
    return value, 0

def score(row, model, rule, constant=0.5):
    try:
        orders, orders_missing = get_feature(row, "orders_30d")
        p = model(orders, orders_missing)
        if math.isfinite(p):
            return p
    except Exception:
        stats["model_error"] += 1
    try:
        stats["rule"] += 1
        return rule(row)
    except Exception:
        stats["constant"] += 1
        return constant

model = lambda orders, missing: 0.2 if missing else min(1.0, orders / 10)
assert score({"orders_30d": 5}, model, lambda r: 0.3) == 0.5
assert score({}, model, lambda r: 0.3) == 0.2
assert score({}, lambda o, m: 1 / 0, lambda r: r["x"]) == 0.5
print(dict(stats))
```

The final constant must be unable to fail.

## What to say in the interview

"For a missing feature I use an explicit default together with a missing flag, so the model and I can tell unknown from zero. I count the null rate per feature, because a jump in one feature is the earliest warning. If the model fails I fall back to a rule and then to a constant that cannot raise, and every step has a counter. I would also decide whether to fail open or closed: for a payment I refuse, for a restaurant ranking I serve a generic default."
