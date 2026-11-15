# Proving it with tests

## What it is

A test calls your function on chosen inputs and fails loudly if the answer is wrong. With pytest, a test is a function named `test_...` in a file named `test_*.py`, using a plain `assert`. A fixture shares setup, `parametrize` runs one body over a table of cases, and `pytest.raises` checks that the right error appears. See [pytest basics](#/kb/test-pytest-basics), [Parametrize](#/kb/test-parametrize), [Fakes and monkeypatch](#/kb/test-fakes-monkeypatch), [What to test](#/kb/test-what-to-test) and [Verifying AI-written code](#/kb/ai-verifying-ai-code).

## How it breaks in production

Tests lie in four ways. They cannot fail: `assert slugify("a b")` is true for any non-empty string. They copy the logic, so the bug cancels out. They cover only the happy path, so an empty batch or a `NaN` crashes in production. Or they are flaky, because they use the real clock, a real sleep or unseeded randomness. Tests an assistant writes add one more fault: generated from the code, they confirm what the code does, not what it should do.

## The defence in code

Save this as `test_batch.py` and run `uv run pytest -q`.

```python
import pytest


def batch_split(items, size):
    if size <= 0:
        raise ValueError("size must be positive")
    return [items[i:i + size] for i in range(0, len(items), size)]


@pytest.mark.parametrize("items, size, expected", [
    ([1, 2, 3, 4], 2, [[1, 2], [3, 4]]),   # normal
    ([1, 2, 3], 2, [[1, 2], [3]]),          # smaller last batch
    ([], 3, []),                            # empty
])
def test_batch_split(items, size, expected):
    assert batch_split(items, size) == expected


@pytest.mark.parametrize("bad", [0, -1])
def test_rejects_bad_size(bad):
    with pytest.raises(ValueError, match="positive"):
        batch_split([1], bad)


@pytest.fixture
def data():
    return [1, 2, 3]            # fresh list per test


def test_input_not_modified(data):
    batch_split(data, 2)
    assert data == [1, 2, 3]
```

Choose cases in three groups: the behaviours in the prompt, the edges (empty, one item, the limit, duplicates), and the failure paths with the exact error. Write expected values by hand. Pass in a fake sleep or clock so no test waits; `monkeypatch` is the fallback.

To judge a test an assistant wrote, break the code on purpose, for example change `<` to `<=`, and see whether a test goes red. Then look for an empty input, a bad input, an exact boundary, a narrow `raises` and no real clock.

## What to say in the interview

"I pick tests in three groups: the behaviours in the prompt, the edges, and the failure paths with the exact exception. I write expected values by hand and use parametrize for the table. Time and sleep are injected, so nothing waits. For a test the assistant wrote, I break the code on purpose and check that it fails, and I look for the missing empty, invalid and boundary cases."
