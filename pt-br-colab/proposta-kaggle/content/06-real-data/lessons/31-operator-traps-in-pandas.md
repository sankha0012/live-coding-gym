# Operator traps in pandas and NumPy

Libraries such as pandas and NumPy overload Python's operators. `df["total"] > 100` does not return `True` or `False`: it returns a whole Series of booleans. That is what makes them powerful, and it is also where a lot of silent bugs in ML pipelines come from.

## `and`, `or`, `not` do not work on Series

```python
df[df.total > 100 and df.status == "delivered"]
# ValueError: The truth value of a Series is ambiguous.
```

Python's `and` asks for one boolean. Use the element-wise operators instead: `&` (and), `|` (or), `~` (not).

## Parentheses are required

`&` and `|` bind tighter than `>` and `==`, so without parentheses the expression is grouped as `df.total > (100 & df.status) == "delivered"`, which raises an error or, worse, filters the wrong rows:

```python
df[df.total > 100 & df.status == "delivered"]       # wrong
df[(df.total > 100) & (df.status == "delivered")]   # right
```

## NaN is not equal to anything, including itself

```python
np.nan == np.nan          # False
s == np.nan               # all False, always
s == None                 # all False for NaN in a float column
s.isna()                  # the right test
```

Two prediction columns that both hold NaN on the same row are "different" for `!=`. When you compare an old and a new model (shadow mode), handle that case explicitly.

## Comparisons with NaN are False

`s > 100` is False where `s` is NaN, and so is `s <= 100`. A filter and its "opposite" do not add up to the whole table when there are missing values. Count `s.isna()` before you trust a split.

## Missing values change dtypes

One missing value turns an integer column into `float64`, because NaN is a float. IDs like `1234` become `1234.0` and stop matching in joins. Use the nullable `Int64` dtype or fill before casting.

## Aggregates skip NaN quietly

`s.mean()` and `s.sum()` skip NaN by default. `len(s)` counts every row, while `s.count()` counts only the non-missing ones. A mean over 10 valid values out of 1,000 rows looks just as confident as a mean over 1,000.

## Chained assignment does not write back

Since pandas 3.0, copy-on-write is always on: every filtered frame behaves as a copy.

```python
df[df.total > 100]["flag"] = 1     # df is NOT changed (ChainedAssignmentError warning)
df.loc[df.total > 100, "flag"] = 1 # changes df
big = df[df.total > 100]
big["flag"] = 1                    # changes big only, never df
```

On pandas 2.x the same code gave a `SettingWithCopyWarning` and its effect depended on the case, so older code and tutorials still show `.copy()` everywhere. Writing `.copy()` when you mean a new frame is still a clear way to show intent.

## Saying it in the interview

"I'm using `&` with parentheses because pandas overloads the operators, and I'm checking `isna()` explicitly because NaN fails every comparison" shows that you know where the data can bite.
