# Leakage and time-based splits

## What it is

Leakage is information in the features that you will not have at prediction time: the future, or the answer itself. It makes validation scores too good. A time-based split avoids part of it: train on the past, test on the future, as production will. See [train/test split and leakage](#/kb/ml-train-test-split-leakage), [time splits](#/kb/pd-time-split-leakage) and [pipelines](#/kb/ml-sklearn-pipeline).

## How it breaks in production

- **Random split on time data.** Neighbouring days land in both sets and the model memorises the period. The reported score is higher than the live score.
- **Fitting before splitting.** A scaler, imputer or target encoding learned on the whole table has seen the test rows.
- **Features from after the event.** A payment confirmation or final status used to predict the payment is a copy of the label.
- **Overlapping windows.** A 7-day rolling feature at the cut date reaches into the test period.

## The defence in code

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

d = pd.DataFrame({"day": pd.date_range("2026-01-01", periods=10),
                  "x": np.arange(10.0),
                  "y": [0, 0, 1, 0, 1, 1, 0, 1, 1, 1]})

def time_split(df, col, cut, gap_days=0):
    df = df.sort_values(col)
    train = df[df[col] < cut - pd.Timedelta(days=gap_days)]
    test = df[df[col] >= cut]
    assert train[col].max() < test[col].min()
    return train, test

train, test = time_split(d, "day", pd.Timestamp("2026-01-08"), gap_days=1)
print(len(train), len(test))                       # 6 3

d["label_mean"] = d.groupby("y")["x"].transform("mean")   # leaks the label
print(d.corr().round(2)["y"].to_dict())

for tr, te in TimeSeriesSplit(n_splits=3).split(d):
    print(tr.tolist(), te.tolist())
```

The function sorts, cuts on a date, leaves a gap for look-back features and asserts that train ends before test starts. With a 1-day gap, 6 rows train and 3 test. The `label_mean` column is built from the target, so its correlation with `y` is exactly 1.0, the signature of a leak: a feature that is suspiciously perfect. `TimeSeriesSplit` makes growing training windows that always precede the test block, but it assumes the rows are already sorted. For imputers and scalers, put them in a `Pipeline` so each fold fits on its own training part.

## What to say in the interview

"For data ordered in time I split by date, leave a gap if features look back, and assert that the latest training date is before the earliest test date. I fit every transformation on training data only, inside a pipeline. For each feature I ask whether I would know it at prediction time, and I treat a near-perfect feature as a bug until proven otherwise."
