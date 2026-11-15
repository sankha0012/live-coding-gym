---
title: Floats, NaN, infinity and rounding
summary: Why 0.1 + 0.2 is not 0.3, how NaN and infinity behave, and how round, floor and // really work.
tags: [python, numbers, floats]
---
```python
import math
0.1 + 0.2 == 0.3               # False   0.1 + 0.2 is 0.30000000000000004
math.isclose(0.1 + 0.2, 0.3)   # True    compare floats with a tolerance
nan = float("nan")
nan == nan                     # False   NaN is not equal to anything
math.isnan(nan)                # True    the only reliable test
round(2.5), round(3.5)         # (2, 4)  ties go to the even number
-7 // 2, int(-3.5)             # (-4, -3)   // rounds down, int() cuts toward zero
```

- Never test floats with `==`. Use `math.isclose` or `abs(a - b) < 1e-9`.
- Test for NaN with `math.isnan(x)`, never with `x == float("nan")`.
- `round` uses banker's rounding: a tie goes to the nearest even number.

<!-- more -->

## Details

Floats are stored in binary, so most decimal fractions are only approximate. That is why `round(2.675, 2)` gives `2.67`: the stored value is slightly below 2.675.

Ways to turn a float into an integer:

```python
math.floor(-1.5)   # -2   toward minus infinity
math.ceil(1.2)     # 2    toward plus infinity
int(-1.5)          # -1   toward zero
round(-2.5)        # -2   nearest, ties to even
```

`/` always returns a float (`7 / 2` is `3.5`). `//` is floor division (`7 // 2` is `3`). `%` takes the sign of the divisor, so `-7 % 3` is `2`. `divmod(7, 2)` returns `(3, 1)`.

Infinity is `float("inf")` or `math.inf`. It is larger than every number, which makes it a good starting value when you search for a minimum. `math.inf - math.inf` is NaN. `math.isfinite(x)` is `False` for both infinity and NaN.

NaN breaks ordering silently, and the result depends on where it sits:

```python
max([1.0, nan, 3.0])     # 3.0
max([nan, 1.0, 3.0])     # nan
sorted([3.0, nan, 1.0])  # [3.0, nan, 1.0]   not sorted at all
clean = [x for x in [1.0, nan, 3.0] if not math.isnan(x)]   # [1.0, 3.0]
```

Filter NaN out before you sort, sum or take a maximum.

Division by zero raises `ZeroDivisionError`, also for floats. `math.sqrt(-1)` raises `ValueError`.

For money use integers (cents) or `decimal.Decimal("0.1")` built from strings.

## Common mistakes

- Writing `if x == float("nan")`. It is always `False`.
- Expecting `round(2.5)` to be `3`. It is `2`.
- Using `int(x)` when you need `math.floor(x)` for negative numbers.
- Comparing a computed float to a constant with `==` in a test. Use `pytest.approx` or `math.isclose`.
- Calling `sorted` or `max` on data that may contain NaN.

## See also

- [f-strings and number formatting](#/kb/py-f-strings)
- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- [Missing values: isna, fillna, dropna](#/kb/pd-missing-values)
- Official docs: https://docs.python.org/3/library/math.html
