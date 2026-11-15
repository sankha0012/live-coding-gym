---
title: Fakes, fake clocks and monkeypatch
summary: Replace time, sleep, the network or the environment in tests so they run fast and give the same result.
tags: [testing, pytest, fakes]
---
```python
class FakeClock:                       # a fake: a small working stand-in
    def __init__(self): self.now = 0.0
    def __call__(self): return self.now
    def advance(self, s): self.now += s

def is_expired(created, ttl, clock):   # the clock is a parameter
    return clock() - created >= ttl
def test_expires_after_ttl():
    clock = FakeClock()
    assert not is_expired(0.0, 60, clock)
    clock.advance(60)                  # no real waiting
    assert is_expired(0.0, 60, clock)
```

- Pass the clock, sleep function or client in as a parameter. Tests pass a fake, real code passes the real one.
- A test must never really sleep or call the network.
- When you cannot change the signature, use the `monkeypatch` fixture. It undoes its changes after each test.

<!-- more -->

## Details

**Injection with a default.** The real function is the default value, so callers do not change:

```python
import time

def wait_and_double(x, sleep=time.sleep):
    sleep(5)
    return x * 2

def test_no_real_sleep():
    naps = []
    assert wait_and_double(2, sleep=naps.append) == 4
    assert naps == [5]                 # it asked for 5 seconds, and took none
```

A list's `append` is the smallest fake: it records every call. A fake for a service is a small class with the same methods that returns prepared answers, or raises on the first call to simulate a failure.

**monkeypatch** replaces things for one test only:

```python
import os

def test_patched(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 1000.0)
    monkeypatch.setenv("MODE", "test")
    monkeypatch.delenv("API_KEY", raising=False)
    assert time.time() == 1000.0
    assert os.environ["MODE"] == "test"
```

Other helpers: `monkeypatch.setitem(some_dict, key, value)` and `monkeypatch.chdir(path)`.

**Patch where the name is looked up.** If `app.py` has `from time import sleep`, then `app` owns its own name `sleep`. Patch `app.sleep`, not `time.sleep`. If `app.py` has `import time` and calls `time.sleep(...)`, patching `time.sleep` works.

Prefer injection in code you write. It needs no framework, and the dependency is visible in the signature.

## Common mistakes

- Calling `time.sleep` or `time.time` directly deep inside the logic, so tests are slow or random.
- Patching the wrong module, so the real function still runs.
- Setting `os.environ[...]` or a module attribute by hand and never restoring it. The change leaks into later tests.
- A fake that copies the logic under test. Keep fakes dumb: fixed values and recorded calls.
- Advancing a fake clock by less than the limit and expecting expiry. Test just below the limit and exactly at it.

## See also

- [Clocks: time.monotonic and injecting a clock or sleep](#/kb/py-time-clock-injection)
- [Fixtures and tmp_path](#/kb/test-fixtures)
- [Retries with backoff](#/kb/prod-retry-backoff)
- Official docs: https://docs.pytest.org/
