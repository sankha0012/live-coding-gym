# Testing failures and time

## The problem it solves

The hard bugs in production code live in the failure paths: a bad input must raise the right error, a retry must wait and then give up, a call to a remote service must survive a timeout. These paths are also the hardest to test, because the real service is slow, the real clock moves, and real failures do not happen on demand.

Three tools solve this: `pytest.raises` for expected errors, a fake clock for time, and `monkeypatch` to replace a real dependency with a fake one.

## The smallest runnable example

```python
import pytest


def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise ValueError("insufficient funds")
    return balance - amount


def test_withdraw_ok():
    assert withdraw(100, 30) == 70


def test_withdraw_too_much():
    with pytest.raises(ValueError, match="insufficient"):
        withdraw(10, 50)


def test_withdraw_zero():
    with pytest.raises(ValueError, match="positive"):
        withdraw(10, 0)
```

`pytest.raises` passes if the block raises that exception type, and fails if it raises nothing or a different type. The optional `match` is a regular expression checked against the message, so you know it is the right error and not another `ValueError` from somewhere else. Use the narrowest type you can. `pytest.raises(Exception)` accepts almost any bug.

## A fake clock for retry and timeouts

Never let a test really sleep. Pass the sleep function in, and give the test a fake that records the waits:

```python
import pytest


def retry(fn, attempts, delay, sleep):
    for i in range(attempts):
        try:
            return fn()
        except ConnectionError:
            if i == attempts - 1:
                raise
            sleep(delay * 2 ** i)


def test_retry_waits_with_backoff_then_succeeds():
    waits = []
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("down")
        return "ok"

    assert retry(flaky, attempts=5, delay=1, sleep=waits.append) == "ok"
    assert waits == [1, 2]


def test_retry_gives_up_after_last_attempt():
    def always_down():
        raise ConnectionError("down")

    waits = []
    with pytest.raises(ConnectionError):
        retry(always_down, attempts=3, delay=1, sleep=waits.append)
    assert waits == [1, 2]
```

The test runs in microseconds and checks the exact waits. For "now" values, pass the time as an argument or a callable in the same way.

## monkeypatch for code you cannot change

Sometimes the function reads the clock or calls a service directly, and you cannot add a parameter. `monkeypatch` replaces an attribute for one test and puts it back afterwards:

```python
import time


def age_label():
    return "old" if time.time() > 1000 else "new"


def test_age_label_old(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 5000.0)
    assert age_label() == "old"


def test_age_label_new(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 10.0)
    assert age_label() == "new"
```

It also has `monkeypatch.setenv("NAME", "value")` for environment variables and `monkeypatch.setitem` for dicts. Patch the name where the code looks it up. If a module did `from time import time`, patch `module.time`, not `time.time`.

Passing the dependency as an argument is cleaner, because the signature shows it. Use `monkeypatch` when you must test code as it is.

## Three traps people hit

1. **`pytest.raises` that is too wide.** `with pytest.raises(Exception)` passes when your code has a typo and raises `NameError`. Name the exact type and add `match`.
2. **Code after the raising line.** Inside a `with pytest.raises` block, the first line that raises ends the block. Lines after it never run, so an assert placed there is dead. Put asserts about the error on the `excinfo` object after the block, or in a separate statement.
3. **Patching the wrong name.** If the code imported `sleep` into its own module, `monkeypatch.setattr(time, "sleep", ...)` changes nothing for it. The test then sleeps for real, or checks nothing. Patch where the name is used, and check the test is fast.

## Why this matters in an interview

The prompt for an ML-systems task nearly always mentions retries, timeouts, bad rows or a missing service. If you show a test that fakes the failure and checks the exact behaviour, you prove the code handles it, not just that you wrote a `try`.

## Say it like this

"For failure paths I use pytest.raises with the exact exception and a match on the message. For anything with time I pass in a fake sleep or clock, so the test is instant and I can assert the exact waits. If I cannot change the code, I use monkeypatch to replace the clock or the service for that one test. I always check that the test fails when I remove the error handling, so I know it really covers the path."
