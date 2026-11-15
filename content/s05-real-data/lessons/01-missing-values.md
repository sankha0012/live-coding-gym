# Missing values and how to fill them

## What it is

A missing value is a cell with no data: `NaN` or `None` in pandas, `NULL` in SQL. It appears for different reasons. A cancelled order has no delivery time, a customer never answered a survey, a service timed out and returned nothing. The reason matters, because it decides what you should do. See also [missing values in pandas](#/kb/pd-missing-values).

## How it breaks in production

- **Silent skipping.** `mean()` and `sum()` skip `NaN`, so a rate looks healthy while it is computed on a fraction of the rows.
- **Fake values.** Filling a missing delivery time with 0 says the order arrived instantly, and the model learns it.
- **Comparisons.** `NaN == NaN` is `False`, so `df["x"] == np.nan` never matches. Use `isna()`.
- **Type change.** One `NaN` turns an integer column into float.
- **Leaky fills.** A median computed on the whole table before splitting lets the test rows shape the fill value.

## The defence in code

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "status": ["delivered", "delivered", "cancelled", "delivered", "cancelled"],
    "minutes": [30.0, np.nan, np.nan, 45.0, np.nan],
})
print(df["minutes"].mean(), df["minutes"].count(), len(df))   # 37.5 2 5
print(df.groupby("status")["minutes"].apply(lambda s: s.isna().mean()))

def fill_with_flag(train, other, col):
    fill = train[col].median()          # statistic from train only
    out = other.copy()
    out[col + "_missing"] = out[col].isna()   # keep the signal
    out[col] = out[col].fillna(fill)
    return out, fill

out, fill = fill_with_flag(df.iloc[:3], df.iloc[3:], "minutes")
print(fill)
print(out)
```

The mean is 37.5 but only 2 of 5 rows contributed, so I print `count()` next to it. Cancelled orders are 100% missing and delivered ones 33%, so the holes are not random. The function computes the fill on the training rows (30.0) and applies it to the other rows, and the flag column keeps the fact that the value was missing. In scikit-learn, `SimpleImputer` does the same: `fit` on train, `transform` on both.

## What to say in the interview

"First I count the missing values per column and check whether they depend on another column, for example cancelled orders have no delivery time. Then I choose per column: drop if few and random, a constant if the hole truly means zero, or a statistic plus a missing flag if the hole carries signal. I compute the fill value on the training data only, and I always report how many rows a mean was computed on."
