# Missing values

## The problem it solves

Real tables have holes. A delivery time is empty because the order was cancelled. A rating is empty because the customer never answered. A price is empty because a service failed. If you do not decide what an empty cell means, pandas decides for you, and its choices are quiet. Sums skip the holes, means skip the holes, and a model may crash or learn the wrong thing.

Your job in a live round is to say three things out loud: how many are missing, why they are missing, and what you do about it.

## The smallest runnable example

```python
import numpy as np
import pandas as pd

df = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5],
    "status": ["delivered", "delivered", "cancelled", "delivered", "cancelled"],
    "minutes": [30.0, np.nan, np.nan, 45.0, np.nan],
    "tip": [5.0, 0.0, np.nan, np.nan, np.nan],
})

print(df.isna().sum())                 # count per column
print(df.isna().mean())                # share per column
print(df["minutes"].mean())            # NaN is skipped: mean of 30 and 45
print(df["minutes"].sum())             # 75.0
print(df["minutes"].count())           # counts only non-null: 2
print(len(df["minutes"]))              # 5
```

Run it and read the numbers. `mean()` gives 37.5, because only two values count. `count()` is 2 and `len()` is 5. That gap is the whole lesson in one line.

Now look at why they are missing:

```python
print(df.groupby("status")["minutes"].apply(lambda s: s.isna().mean()))
```

Cancelled orders are always missing a delivery time, and some delivered ones are too. The first kind is expected. The second kind is a data problem. They need different treatment.

## Three ways to handle a hole

```python
clean = df.dropna(subset=["minutes"])               # drop rows
filled = df["tip"].fillna(0)                        # constant
median = df["minutes"].fillna(df["minutes"].median())  # a statistic
df["minutes_missing"] = df["minutes"].isna()        # keep the signal
```

Dropping is fine when few rows are affected and the missing rows are not special. A constant is right when the hole really means zero, such as no coupon. A statistic is a guess, so say it is a guess. A flag column keeps the fact that the value was missing, which is often predictive on its own.

## The three traps

**Trap 1: the denominator.** `mean()` skips nulls, so a rate can look better than it is. If 3 of 5 orders have no delivery time, the average of the other two says nothing about those three. Always print the count next to the mean.

**Trap 2: filling with a number that means something.** Filling a missing delivery time with 0 says the order arrived instantly. Filling with the overall mean hides the fact that cancelled orders are different. A fill value must not look like real data. When the hole is informative, use a flag column, or leave it as NaN and let the model handle it. Some models, like gradient boosting in scikit-learn's `HistGradientBoostingClassifier`, accept NaN directly.

**Trap 3: filling before splitting.** If you compute the median on the whole table and then split into train and test, the test rows influenced the fill value. That is a small leak. Compute the fill value on the training part only and reuse it:

```python
train = df.iloc[:3]
test = df.iloc[3:]
fill = train["minutes"].median()        # from train only
test_filled = test["minutes"].fillna(fill)
print(fill, test_filled.tolist())
```

In scikit-learn the same idea is `SimpleImputer`: call `fit` on train, then `transform` on both.

## More small facts worth knowing

`NaN` is never equal to itself, so `df["x"] == np.nan` is always False. Use `isna()`. In pandas, `np.nan` in an integer column turns it into float, which is why a count column suddenly shows `3.0`. The nullable type `"Int64"` keeps integers with holes. Empty strings are not null: `""` stays in the column after `isna()` says zero. Check with `df["x"].eq("").sum()`, and convert them with `replace("", np.nan)`.

In SQL the same trap exists: `AVG(col)` skips NULL, and `COUNT(col)` counts only non-null while `COUNT(*)` counts rows.

## Say it like this

"First I count the missing values per column and look at whether they depend on another column, for example cancelled orders have no delivery time. That tells me if the hole is expected or a data bug. Then I choose per column: drop if few and random, fill with a constant if the hole truly means zero, and add a missing flag if the hole carries signal. I never fill with a value that looks real, and I compute any fill statistic on the training data only, to avoid leakage. And I always report how many rows a mean was computed on."
