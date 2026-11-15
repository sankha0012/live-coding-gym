---
title: Testing exceptions with pytest.raises
summary: Check that code raises the right exception, and the right message, with a with pytest.raises block.
tags: [testing, pytest, exceptions]
---
```python
import pytest

def parse_age(text):
    age = int(text)                      # ValueError for "abc"
    if age < 0:
        raise ValueError("age must be >= 0")
    return age

def test_rejects_negative():
    with pytest.raises(ValueError, match="must be >= 0"):
        parse_age("-1")
```

- The test passes only if the block raises that exception type, or a subclass of it.
- If nothing is raised, the test fails with `DID NOT RAISE`.
- `match` is a regular expression searched in the message. It does not need to match the whole text.

<!-- more -->

## Details

Put only the call that should fail inside the block. Lines after the raising call never run:

```python
def test_only_the_failing_call_inside():
    text = "abc"                         # setup stays outside
    with pytest.raises(ValueError):
        parse_age(text)
```

To inspect the exception, name it with `as`. Read it **after** the block:

```python
def test_message_names_the_rule():
    with pytest.raises(ValueError) as excinfo:
        parse_age("-5")
    assert "must be >= 0" in str(excinfo.value)
    assert excinfo.type is ValueError
```

`excinfo.value` is the exception object, so custom attributes such as `excinfo.value.code` can be checked too.

Because `match` uses `re.search`, characters such as `(`, `.` and `+` have a special meaning. Wrap literal text in `re.escape`:

```python
import re

def test_literal_message():
    with pytest.raises(ValueError, match=re.escape("age must be >= 0")):
        parse_age("-1")
```

A tuple accepts several types: `pytest.raises((KeyError, IndexError))`.

Ask for the most specific type you can. `pytest.raises(Exception)` also passes on a `TypeError` caused by a typo in your own test.

Failure paths go well with `parametrize`: one row per bad input.

## Common mistakes

- Putting an `assert` inside the block after the raising call. It never runs, so it checks nothing.
- Catching too wide a type, such as `Exception`, which hides real bugs.
- Using `try` and `except` with no `else` branch, so the test passes when nothing is raised.
- Forgetting that `match` is a regex. `match="(empty)"` does not look for brackets.
- Reading `excinfo.value` inside the `with` block, before the exception exists.

## See also

- [Exceptions: try, except, raise, custom errors](#/kb/py-exceptions)
- [pytest.mark.parametrize](#/kb/test-parametrize)
- [What to test: behaviours, edges, failure paths](#/kb/test-what-to-test)
- Official docs: https://docs.pytest.org/
