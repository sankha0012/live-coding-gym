# Label leakage

## What it is

Label leakage means a feature contains information that would not be available at prediction time, usually because it was created from the answer or from the future. The model learns to read the answer instead of predicting it. Typical examples are a "refund issued" column in a model that predicts refunds, an aggregate computed over the whole dataset including the test rows, a scaler fitted before the train and test split, or a random split on time-ordered data. See [train/test split leakage](#/kb/ml-train-test-split-leakage) and [time-based leakage](#/kb/pd-time-split-leakage).

## How it breaks in production

Offline metrics are excellent, sometimes suspiciously perfect, and production quality is poor because the leaked feature does not exist, or is empty, when the model runs live. Nothing fails loudly. The team has already celebrated and shipped. A useful reflex: a validation score of 0.99 on a hard problem is a warning, not a win. Leakage also hides in preprocessing: fitting an imputer or scaler on the full dataset lets the test set influence training.

## The defence in code

Split first and fit only on training data. For time-ordered data, split by time. A quick scan for a feature that almost equals the label catches the crudest leaks.

```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
n = 500
df = pd.DataFrame({
    "day": np.arange(n),
    "x": rng.normal(size=n),
})
df["y"] = (df["x"] + rng.normal(scale=2, size=n) > 0).astype(int)
df["refund_flag"] = df["y"]  # leaked: built from the label

def leak_scan(df, label, threshold=0.95):
    corr = df.drop(columns=[label]).corrwith(df[label]).abs()
    return sorted(corr[corr > threshold].index)

assert leak_scan(df, "y") == ["refund_flag"]

# time split: train strictly before the cutoff, test after it
cutoff = 400
train, test = df[df["day"] < cutoff], df[df["day"] >= cutoff]
assert train["day"].max() < test["day"].min()
mean_train = train["x"].mean()  # fit statistics on train only
print(len(train), len(test), round(mean_train, 3))
```

Correlation only finds the obvious leaks. Features that leak through time or grouping need a question, not a formula: for every feature, could I know this value at the moment of prediction?

## What to say in the interview

"If an offline score looks too good, I look for leakage before anything else. I would ask for each feature whether it is known at prediction time, split by time when the data is ordered, and fit scalers and imputers on the training part only. A quick correlation scan with the label catches the crude cases, but the real check is that question about timing."
