# Verifying AI code

## The problem it solves

AI code often looks right and runs on the happy path. The bugs sit in the places you did not ask about. In the interview you are judged on whether you noticed them. Accepting the first answer without checking is the most common way to lose points. Verifying is a short routine, and you can do it in a few minutes.

The routine has four steps:

1. **Read every line.** Out loud if you can. If you cannot explain a line, ask the assistant or rewrite it.
2. **Run the tests.** Yours, not only the ones the assistant wrote. Its tests may check what its code does, not what you asked for.
3. **Try three edge inputs.** Empty, one item, and a bad value such as None or NaN.
4. **Check the usual mistakes** listed below.

## The smallest runnable example

Suppose the assistant wrote this to split a list into chunks of size n:

```python
def chunk(items, n):
    return [items[i:i + n] for i in range(0, len(items) - n, n)]
```

It looks fine. Run an ordinary input and two edge inputs:

```python
def chunk(items, n):
    return [items[i:i + n] for i in range(0, len(items) - n, n)]


print(chunk([1, 2, 3, 4], 2))   # expected [[1, 2], [3, 4]]
print(chunk([1], 2))            # expected [[1]]
print(chunk([], 2))             # expected []
```

The first call prints `[[1, 2]]` and loses the last chunk. The range stops at `len(items) - n`, which is one whole chunk too early. The second call prints `[]` and loses the only item. The fix is to go up to `len(items)`:

```python
def chunk(items, n):
    if n < 1:
        raise ValueError("n must be at least 1")
    return [items[i:i + n] for i in range(0, len(items), n)]


assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]
assert chunk([1], 2) == [[1]]
assert chunk([], 2) == []
print("ok")
```

Running three inputs found the bug in seconds. Reading the code line by line should catch it too, but only if you check where the range ends.

## The usual AI mistakes

Keep this list in your head and scan for each one:

- **Off by one** in ranges, slices and chunk boundaries.
- **Mutable default argument**, such as `def f(x, seen=[])`. The list is shared between calls.
- **NaN comparisons.** `nan == nan` is False, and `nan < 1` is False, so filters and sorts misbehave.
- **Naive datetimes.** Mixing timezone-aware and naive values raises an error or gives wrong hours.
- **Swallowed exceptions.** A bare `except: pass` hides real failures.
- **Data leakage.** Fitting a scaler on all data before the train and test split.
- **Mutating the input** when the prompt said not to.
- **Wrong tie behaviour** in sorting and ranking.

## The three traps

**1. Trusting the assistant's tests.** If the code is wrong and the test was written from the code, both agree and both are wrong. Write at least one assert from your own prompt, before you read the code.

**2. Testing only the happy path.** One normal example proves little. The three edge inputs take a minute and catch most bugs.

**3. Fixing by guessing.** When a test fails, do not paste the error back and hope. Find the line, say why it is wrong, then fix it or tell the assistant exactly what to change. The interviewer watches how you debug.

## Say it like this

"I read the generated code line by line and match each line to a rule in my prompt. Then I run the tests, and I add three edge inputs: empty, a single item, and a bad value like NaN. I also look for the usual mistakes: off by one, mutable defaults, swallowed exceptions and data leakage. Here the chunk loop stopped one step early, so I fixed the range and added a test for it. I would rather find the bug myself than let the interviewer find it."
