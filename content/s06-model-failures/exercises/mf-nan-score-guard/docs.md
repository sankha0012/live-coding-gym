# guard_scores reference

## Contract

`guard_scores(scores: list, fallback: float = 0.5) -> tuple[list[float], int]`

Input is a list of anything a model might emit. Output is `(clean_scores, bad_count)`: a new list of the same length and order, plus how many entries were replaced.

A score is bad when it is `None`, NaN, `inf`, `-inf`, a non-number (including strings such as `"0.7"`, which are never parsed), or a `bool` (`True` and `False` are bad). Every other number is good and is returned unchanged, even if it is outside 0 to 1 or is an int.

```
guard_scores([0.2, None, float("nan"), 3], fallback=0.0)
# ([0.2, 0.0, 0.0, 3], 2)
```

The input list is not modified. An empty list gives `([], 0)`.

## Library notes

- `math.isnan(x) -> bool`: True only for NaN. It raises `TypeError` for a string or `None`, so it cannot be your first check on untrusted values.
- `math.isfinite(x) -> bool`: False for NaN, `inf` and `-inf`. It also raises `TypeError` on strings, and returns True for `True`.
- `isinstance(x, numbers.Real) -> bool`: True for int, float and numpy scalars such as `np.int64`. Gotcha: `bool` is a subclass of `int`, so `isinstance(True, int)` is True.
- NaN is never equal to itself, so `x == nan` is always False. `x != x` is True only for NaN, but `in` can still match by object identity, so do not rely on it.

## Gotchas

- Silently replacing bad scores hides a broken model. The count is what lets a caller alert on it, so keep it accurate.
- A fallback that looks like a real score can distort metrics downstream. Log the count next to the output.
- Check the type before the value. Order matters because value checks crash on types they do not expect.
