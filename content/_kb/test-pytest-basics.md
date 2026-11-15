---
title: pytest basics
summary: Write functions named test_ with plain assert statements; pytest finds them, runs them and reports.
tags: [testing, pytest, assert]
---
```python
# test_cart.py   (file name and function names start with test_)
def total(prices):
    return sum(prices)

def test_total_adds_prices():
    assert total([2, 3]) == 5

def test_total_of_empty_is_zero():
    assert total([]) == 0

# run:  pytest -q     ->  2 passed
```

- pytest collects files named `test_*.py` and functions named `test_*`. No class is needed.
- Use a plain `assert`. On failure pytest shows both sides of the comparison.
- One behaviour per test, and name the test after that behaviour.

<!-- more -->

## Details

A test passes when it finishes without an exception. A failed `assert` or any unexpected error fails it.

Usually the code lives in another file and the test imports it: `from cart import total`.

Most tests have three parts: arrange the input, act by calling the code, assert on the result.

Useful command-line options:

| Command | Effect |
|---|---|
| `pytest -q` | short output |
| `pytest -x` | stop at the first failure |
| `pytest -k empty` | run only tests whose name contains `empty` |
| `pytest test_cart.py::test_total_adds_prices` | run one test |
| `pytest -v` | one line per test |
| `pytest -s` | show `print` output |

In this project, run it as `uv run pytest -q`.

Compare floats with `pytest.approx`, not with `==`:

```python
import pytest

def test_float_sum():
    assert 0.1 + 0.2 == pytest.approx(0.3)
```

A failure report shows the values:

```
>       assert total([2, 3]) == 6
E       assert 5 == 6
E        +  where 5 = total([2, 3])
```

Read the `E` lines first. The left side is what the code returned, the right side is what the test expected.

You can add a message: `assert rows, "expected at least one row"`.

## Common mistakes

- Naming the file `cart_test_cases.py` or the function `check_total`. pytest does not collect them and reports nothing.
- Writing `total([2, 3]) == 5` without `assert`. The line does nothing and the test passes.
- Writing `assert (x == 1, "message")`. A non-empty tuple is always true. Remove the parentheses.
- Putting many unrelated checks in one test. The first failure hides the rest.
- Tests that depend on each other's leftovers. Each test must build its own data.

## See also

- [pytest.mark.parametrize](#/kb/test-parametrize)
- [Fixtures and tmp_path](#/kb/test-fixtures)
- [Testing exceptions with pytest.raises](#/kb/test-raises)
- Official docs: https://docs.pytest.org/
