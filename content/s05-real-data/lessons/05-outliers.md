# Outliers

## What it is

An outlier is a value far from the rest. It can be a real rare event, such as a very large corporate order, or an error, such as a price entered in cents instead of reais, a sensor stuck at 9999, or a test order. The first step is never deleting it. The first step is finding out which kind it is. See [outliers](#/kb/pd-outliers).

## How it breaks in production

- **The mean moves.** One value of 500 among values near 25 pulls the mean to 84, and the standard deviation to 168.
- **Z-scores hide themselves.** The outlier inflates the standard deviation, so its own z-score is only 2.5 and a rule like "above 3" misses it.
- **Models and charts.** Linear models and scalers are dragged by extremes, and one huge bar flattens every other bar in a chart.
- **Deleting real signal.** Fraud, big customers and outages are outliers. Removing them hides the thing you were asked to find.

## The defence in code

```python
import pandas as pd

x = pd.Series([20, 25, 30, 28, 22, 26, 24, 500.0])
print(round(x.mean(), 1), x.median(), round(x.std(), 1))   # 84.4 25.5 168.0

q1, q3 = x.quantile([0.25, 0.75])
iqr = q3 - q1
low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
print(low, high)                           # 16.0 36.0
print(x[~x.between(low, high)].tolist())   # [500.0]

def flag_and_clip(s, lo=0.01, hi=0.99):
    a, b = s.quantile([lo, hi])
    return s.clip(a, b), (s < a) | (s > b)

clipped, flagged = flag_and_clip(x)
print(round(clipped.max(), 1), int(flagged.sum()))         # 467.1 2
z = (x - x.mean()) / x.std()
print(round(z.max(), 2))                                   # 2.47
```

The median barely notices the outlier, and the IQR fences (16 to 36) catch 500 because quartiles are not dragged by it. The z-score of 500 is only 2.47, below the usual threshold of 3, so a z-score rule would miss it. The function returns both a clipped copy and a flag, so I keep the evidence. With only 8 values the 1% and 99% percentiles interpolate between neighbours, so clipping moved the maximum to 467.1 and flagged two points. That is a reminder that percentile clipping needs enough data.

## What to say in the interview

"I first ask whether the value is an error or a real rare event, and I look at the rows before touching them. I prefer robust tools such as the median and the IQR fences, because the mean and the z-score are distorted by the very values they are meant to catch. I flag or clip into a new column rather than deleting, and I only remove a value when I can name the cause, such as a unit error."
