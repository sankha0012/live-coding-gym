---
title: "Exceptions: try, except, raise, custom errors"
summary: Catch errors with try and except, signal them with raise, and define your own exception classes.
tags: [python, exceptions, errors]
---
```python
try:
    n = int("abc")
except ValueError as e:
    print("bad input:", e)     # bad input: invalid literal for int() with base 10: 'abc'
else:
    print("ok", n)             # runs only when the try block raised nothing
finally:
    print("always")            # always    runs in every case
raise ValueError("amount must be positive")   # signal an error yourself
```

- Catch the most specific exception you expect. Anything else keeps travelling up.
- `raise SomeError("message")` stops the function at once.
- `else` and `finally` are optional.

<!-- more -->

## Details

Built-in exceptions you will meet most: `ValueError` (right type, bad value), `TypeError` (wrong type), `KeyError` (missing dict key), `IndexError` (list index out of range), `ZeroDivisionError`, `AttributeError`, `FileNotFoundError`.

Catch several types with a tuple, or use several `except` blocks. Python takes the first block that matches, so put specific types before general ones.

```python
def safe_div(a, b):
    try:
        return a / b
    except (ZeroDivisionError, TypeError):
        return None

safe_div(1, 0), safe_div(1, "x"), safe_div(6, 3)   # (None, None, 2.0)
```

A custom error is a class that inherits from `Exception`. An empty body is enough. It lets callers catch your error without catching everything else.

```python
class InsufficientFunds(Exception):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFunds(f"need {amount}, have {balance}")
    return balance - amount

try:
    withdraw(10, 50)
except InsufficientFunds as e:
    print(e)                   # need 50, have 10
```

Inside an `except` block, a bare `raise` re-raises the same error after you have logged or cleaned up. `raise NewError("...") from e` raises a different error and keeps the original as its cause.

Validate inputs at the top of a function and raise early with a clear message. The caller decides what to do with the error.

## Common mistakes

- Using a bare `except:` or `except Exception: pass`. It hides real bugs, including typos.
- Wrapping too much code in one `try`, so you cannot tell which line failed.
- Returning a special value such as `-1` or `None` where the task asks you to raise.
- Raising an error inside a `try` whose own `except` catches it, so the caller never sees it.
- Forgetting that `finally` runs even when the `try` block returns.

## See also

- [Testing exceptions with pytest.raises](#/kb/test-raises)
- [Input validation and data contracts](#/kb/prod-input-validation)
- [Files and pathlib](#/kb/py-files-pathlib)
- Official docs: https://docs.python.org/3/tutorial/errors.html
