# Time-based splits and leakage

## The problem it solves

A model is judged on data it has not seen. In production, "not seen" means the future. If you shuffle rows and split at random, the training set contains days that come after some test days. The model has effectively seen the future, and the score you report is too good. After deployment the real score is lower, and someone asks why.

Leakage is any way that information from outside the training window, or from the target itself, gets into the features. Interviewers love it because the code runs fine and the metric looks great.

## The smallest runnable example

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "day": pd.date_range("2026-01-01", periods=10, freq="D"),
    "x": np.arange(10, dtype=float),
    "y": [0, 0, 1, 0, 1, 1, 0, 1, 1, 1],
})

df = df.sort_values("day")
cut = pd.Timestamp("2026-01-08")
train = df[df["day"] < cut]
test = df[df["day"] >= cut]

print(len(train), len(test))                       # 7 3
print(train["day"].max() < test["day"].min())      # True
```

The rule is simple: sort by time, pick a cut date, train strictly before it, test on or after it. The last line is a cheap check you can keep in the code as an `assert`.

For several folds, scikit-learn has `TimeSeriesSplit`. Each fold trains on the past and tests on the block after it:

```python
from sklearn.model_selection import TimeSeriesSplit

X = df[["x"]].to_numpy()
for tr, te in TimeSeriesSplit(n_splits=3).split(X):
    print(tr.tolist(), te.tolist())
```

It assumes the rows are already sorted by time. It does not check this for you.

## Leakage that is not about the split

```python
rng = np.random.default_rng(0)
d = pd.DataFrame({"x": rng.normal(size=8),
                  "paid": [0, 1, 0, 1, 1, 0, 1, 0]})
d["payment_confirmed"] = d["paid"]     # only known after the outcome
print(d.corr().round(2)["paid"])
```

A feature that is only known after the outcome, such as a payment confirmation, a final status or a delivery time when you predict late delivery, cannot be used. And a feature built from the whole table, like a global target mean, contains the answer for the test rows too.

## The three traps

**Trap 1: random split on time data.** Orders, clicks and payments are ordered in time and behaviour drifts. A random split puts neighbours of the same day in both sets, so the model memorises the period. Split by date. Also keep a gap if your features look back a few days, so the windows do not overlap the test period.

**Trap 2: fitting on everything first.** Scalers, imputers, encoders and target encodings all learn numbers from data. If you call `fit` on the full table and split afterwards, the test rows shaped those numbers. Fit on train only, then `transform` the test. A scikit-learn `Pipeline` does this for you inside each fold, which is the easiest way to be safe.

**Trap 3: features from the future or from the label.** Rolling averages that include the current row or later rows, a "total orders of this customer" that counts orders after the prediction time, or a column that is a proxy for the target. A red flag is a feature with a suspiciously high importance or a score close to perfect. Ask for each feature: would I know this value at the moment I need to predict?

Another quiet leak is duplicates: the same customer or the same row in both train and test. If the unit of prediction is a customer, split by customer, or by time with one row per customer.

## How to check quickly

Print the min and max date of train and test. Compare the score of a random split with a time split: a big drop means the random score was inflated. Drop the top feature and see whether the score collapses. And check that no key appears on both sides when it should not.

## Say it like this

"For anything ordered in time I split by date: train strictly before a cut, test after it, and I assert that the max train date is earlier than the min test date. I fit imputers, scalers and encoders on the training part only, ideally inside a pipeline. For each feature I ask if it would be known at prediction time, and I get suspicious when one feature is nearly perfect. If the random-split score is much higher than the time-split score, that gap is the leakage. The time-split score is the honest estimate of production."
