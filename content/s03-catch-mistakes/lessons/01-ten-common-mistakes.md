# The ten most common mistakes in assistant-written Python

## The problem it solves

Assistant code usually works on the happy path, so you cannot judge it by one run on the example. The same ten mistakes appear again and again. Learn each as a pattern: what it looks like, why it is wrong, and the check that finds it.

## 1. Mutable default argument

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags

print(add_tag("a"))   # ['a']
print(add_tag("b"))   # ['a', 'b']   the default list is shared between calls
```

The default is created once, when the function is defined. Fix: `tags=None`, then `tags = [] if tags is None else list(tags)`. Check: search for `=[]`, `={}` and `=set()` in signatures.

## 2. Off-by-one

```python
def chunks(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs) - n, n)]

print(chunks([1, 2, 3, 4, 5, 6], 2))   # [[1, 2], [3, 4]]  the last chunk is lost
```

`range(0, len(xs) - n, n)` stops one chunk too early; it should be `range(0, len(xs), n)`. Check: say the first and last index out loud, and test lengths that divide evenly and not.

## 3. NaN comparison

```python
x = float("nan")
print(x == x)     # False
print(x == float("nan"))   # False
```

NaN is not equal to anything. Use `math.isnan(x)` or pandas `isna`. Also note `max` and `sort` behave unpredictably with NaN in the data. Check: where could a missing value enter, and what does each comparison do with it?

## 4. Swallowed exceptions

```python
def load(path):
    try:
        return json.load(open(path))
    except Exception:
        return {}
```

A missing file, bad JSON and a typo in the code all look the same: an empty dict. Catch only what you expect (`FileNotFoundError`, `json.JSONDecodeError`), and handle it in a visible way (log, raise, or return a clearly marked result). Check: search for `except`.

## 5. Data leakage

```python
scaler = StandardScaler().fit(X)          # fit on everything
X_train, X_test = train_test_split(scaler.transform(X))
```

The test rows influenced the mean and variance used for training. Split first, fit on the training part only, and use a `Pipeline` so cross-validation repeats this correctly. Check: is every `fit` (and `fit_transform`) called only on the training part, after the split?

## 6. Naive datetimes

```python
from datetime import datetime, timezone
a = datetime.now()                       # naive
b = datetime.now(timezone.utc)           # aware
a < b                                    # TypeError: can't compare offset-naive and offset-aware datetimes
```

Mixing the two raises an error, and using naive local time silently shifts with the server's timezone. Prefer timezone-aware UTC internally. Check: where do datetimes come from and are they all aware?

## 7. Wrong complexity

```python
def dedupe(xs):
    out = []
    for x in xs:
        if x not in out:      # O(n) membership test on a list
            out.append(x)
    return out
```

This is O(n^2). Keep a `set` of seen values (and the list for order) to make it O(n). Similar traps: `list.pop(0)` in a loop (use `collections.deque`), string `+=` in a loop (use `"".join`). Check: ask what the size of the input is and what the loop contains.

## 8. Silently changed behaviour

A request: "make `top_words` faster". The answer is faster, and it now returns ties in a different order, lowercases words, or mutates its argument. Nothing is flagged. Check: compare old and new outputs on the same inputs, including ties and empty inputs, and read the whole diff.

## 9. Invented API

```python
import pandas as pd
df = pd.DataFrame({"a": [1, 2]})
df.sort_by("a")          # AttributeError: no such method; the real one is sort_values
```

The assistant produces plausible names or parameters that do not exist, or that belong to another library or version. Running the code often reveals it, but a rarely executed branch may not. Check: look up any call you do not recognise, and run every branch.

## 10. The test edited to pass

A test fails after a change, and the assistant "fixes" it:

```python
assert top_words("b a b") == ["b", "a"]    # original
assert top_words("b a b") == ["a", "b"]    # edited to match the new output
```

Ask which one is right according to the task, not which one passes. If the code changed behaviour, the code is wrong. Check: in every diff, look for changed expectations in tests.

## A quick scan before you accept anything

```text
signature defaults   ->  =[] / ={} ?
loops and slices     ->  last index right?
comparisons          ->  could a value be NaN or None?
except               ->  specific and visible?
fit / transform      ->  after the split?
datetime             ->  aware or naive?
membership / pop(0)  ->  right complexity?
diff                 ->  anything I did not ask for? any test changed?
unknown calls        ->  do they exist?
```

## Common mistakes in reviewing

- Believing one passing run means it is correct.
- Reading only the new lines and not what they replaced.
- Fixing the symptom (add a `try`) instead of the cause.

## Related

- [Verifying AI-written code](#/kb/ai-verifying-ai-code)
- [Copying and mutability](#/kb/py-copy-mutability)
- [math and NaN](#/kb/py-math-nan)
- [Exceptions](#/kb/py-exceptions)
- [Train/test split leakage](#/kb/ml-train-test-split-leakage)
- [Datetimes](#/kb/py-datetime)
- [Complexity](#/kb/py-complexity)
