# Empty and tiny inputs

## What it is

An empty input is zero rows: no orders today, a filter that matched nothing, a failed upstream job. A tiny input is a handful of rows, such as a restaurant with three orders. Both are normal in production, and code written only for the typical case fails on them. See [input validation](#/kb/prod-input-validation) and [NaN handling in Python](#/kb/py-math-nan).

## How it breaks in production

- **Crashes.** `max([])` raises `ValueError`, `[].index(1)` raises `ValueError`, and `1 / 0` raises `ZeroDivisionError`.
- **Silent NaN.** The mean of an empty list is `nan` with only a warning, and the standard deviation of one value is `nan`. The `nan` then flows into a report or a model.
- **Misleading rates.** A restaurant with 3 orders, all late, has a 100% late rate and tops the "worst restaurants" list.
- **Fake zeros.** The sum of an empty pandas series is `0.0`, which looks like a real measurement.

## The defence in code

```python
import numpy as np
import pandas as pd

def late_rate(late, n_min=20):
    n = len(late)
    if n < n_min:
        return None            # too few to judge, say so explicitly
    return float(np.mean(late))

print(late_rate([]), late_rate([1, 1, 1]), late_rate([1] * 30 + [0] * 70))

empty = pd.Series([], dtype=float)
print(empty.mean(), empty.sum(), empty.max())        # nan 0.0 nan
print(pd.Series([5.0]).std())                        # nan

try:
    max([])
except ValueError as e:
    print("ValueError:", e)

def safe_ratio(num, den, default=0.0):
    return num / den if den else default

print(safe_ratio(3, 0), safe_ratio(3, 4))
```

`late_rate` makes the small-sample decision visible: it returns `None` for 0 or 3 rows and 0.3 for 100 rows, and the caller must handle `None`. On an empty series pandas gives `nan` for the mean, `0.0` for the sum and `nan` for the maximum, so an empty sum looks like a real zero. `safe_ratio` shows a deliberate default for a zero denominator. The right default depends on the business: zero, `None` or an error. What matters is that someone chose it.

## What to say in the interview

"I test every function with zero rows, one row and a typical input before I trust it. For empty input I decide the behaviour on purpose: return a default, return `None`, or raise a clear error. For small groups I attach the count and either hide the rate or mark it unreliable, so three late orders do not outrank three hundred."
