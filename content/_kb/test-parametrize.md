---
title: pytest.mark.parametrize
summary: Run one test function once per row of inputs and expected outputs.
tags: [testing, pytest, parametrize]
---
```python
import pytest

@pytest.mark.parametrize("text, expected", [
    ("abc", "ABC"),
    ("", ""),
    ("a b", "A B"),
])
def test_upper(text, expected):
    assert text.upper() == expected

# pytest -q   ->  3 passed   (one test per row)
```

- First argument: the parameter names in one string. Second: a list with one tuple per case.
- Each row is its own test, so one failing row does not hide the others.
- Use it when the same check repeats with different data, such as normal cases plus edge cases.

<!-- more -->

## Details

The names in the string must match parameters of the test function. With one name, the list holds plain values, not tuples:

```python
@pytest.mark.parametrize("n", [0, 1, 7])
def test_square_is_not_negative(n):
    assert n * n >= 0
```

pytest builds a test id from each row, for example `test_upper[abc-ABC]`. Give readable ids with `pytest.param`:

```python
@pytest.mark.parametrize("text, expected", [
    pytest.param("  hi ", "hi", id="spaces"),
    pytest.param("", "", id="empty"),
])
def test_strip(text, expected):
    assert text.strip() == expected
```

`pytest -v` then prints `test_strip[spaces] PASSED` and `test_strip[empty] PASSED`. Run a single case with `pytest -k spaces`.

Two decorators on one test give every combination:

```python
@pytest.mark.parametrize("a", [1, 2])
@pytest.mark.parametrize("b", [10, 20])
def test_sum_is_positive(a, b):          # 4 tests
    assert a + b > 0
```

Cases that should raise fit well in their own parametrized test with `pytest.raises`. That keeps the happy-path test simple.

Keep the table easy to read. If a row needs a comment to be understood, give it an `id`.

## Common mistakes

- Names that do not match the function's parameters. pytest stops with an error at collection time.
- Writing the names as two strings, `"text", "expected"`. The second string is then taken as the list of cases.
- Forgetting the tuple for one row, or giving a row the wrong number of values.
- Putting logic such as `if expected is None:` in the test body. Split it into two tests.
- Sharing a mutable object between rows and changing it in the test.

## See also

- [pytest basics](#/kb/test-pytest-basics)
- [Testing exceptions with pytest.raises](#/kb/test-raises)
- [What to test: behaviours, edges, failure paths](#/kb/test-what-to-test)
- Official docs: https://docs.pytest.org/
