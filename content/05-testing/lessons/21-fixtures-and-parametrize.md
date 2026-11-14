# Fixtures and parametrize

## The problem it solves

After a few tests you notice two kinds of repetition. First, many tests start with the same setup: build a list, create a fake database, make a config. Second, many tests are the same call with different numbers. Copying and pasting hides mistakes and makes the file long.

Pytest has one tool for each. A fixture shares setup. `parametrize` runs one test body over many inputs.

## The smallest runnable example

```python
import pytest


def clamp(x, low, high):
    return max(low, min(high, x))


@pytest.mark.parametrize(
    "x, expected",
    [
        (5, 5),       # inside the range
        (-1, 0),      # below
        (11, 10),     # above
        (0, 0),       # on the lower edge
        (10, 10),     # on the upper edge
    ],
)
def test_clamp(x, expected):
    assert clamp(x, 0, 10) == expected


@pytest.fixture
def scores():
    return [3, 1, 2]


def test_sorted_does_not_change_input(scores):
    assert sorted(scores) == [1, 2, 3]
    assert scores == [3, 1, 2]


def test_each_test_gets_a_fresh_list(scores):
    scores.append(99)
    assert len(scores) == 4
```

Run it with `uv run pytest -q`. You get five test results from `test_clamp`, one per row, plus two more. If one row fails, pytest names the row, so you see which input broke.

## Parametrize in detail

The first argument is a string of names separated by commas. The second is a list of tuples, one tuple per run. Pytest passes each value to the test function parameter with the same name.

Add `ids` when rows are hard to read in the output:

```python
import pytest


@pytest.mark.parametrize("text, expected", [("", ""), ("A B", "a-b")], ids=["empty", "two-words"])
def test_slug(text, expected):
    assert "-".join(text.lower().split()) == expected
```

Use `parametrize` for data tables: edge values, empty input, and the cases the prompt lists. Do not use it when the checks need different logic. Two different behaviours deserve two tests.

## Fixtures in detail

A fixture is a function with `@pytest.fixture`. A test asks for it by writing its name as a parameter. Pytest calls the fixture and passes in the return value. By default each test gets a new copy, so one test cannot damage the data of another.

When setup needs cleanup, use `yield`. Code before the `yield` is setup, code after it runs when the test ends, even if the test failed:

```python
import pytest


@pytest.fixture
def log_lines():
    lines = []
    yield lines
    lines.clear()


def test_log_collects(log_lines):
    log_lines.append("start")
    assert log_lines == ["start"]
```

Two built-in fixtures you will use a lot are `tmp_path`, a fresh empty folder for files, and `monkeypatch`, covered in the next lesson. Put fixtures shared by many files in a file named `conftest.py`, and pytest finds them without an import.

## Three traps people hit

1. **Sharing mutable state by accident.** If a module-level list is used by several tests, one test changes it and the next one fails or, worse, passes for the wrong reason. Build the data inside a fixture so each test gets its own. Widening a fixture scope with `scope="module"` brings the problem back, so do that only for read-only or expensive objects.
2. **Hiding the data in a fixture.** A test that reads `def test_total(order)` forces the reader to open another place to see the numbers. Use fixtures for plumbing, such as connections and folders. Keep the inputs and the expected answer visible in the test or in the parametrize table.
3. **Too many rows, no thinking.** Twenty near-identical rows do not find more bugs than five chosen ones. Pick one row for each idea: normal, empty, lower edge, upper edge, wrong type, and the case that caused a past bug.

## Why this matters in an interview

A parametrize table is the fastest way to show coverage on screen. The interviewer reads five rows and sees at once which edges you thought of. A short fixture shows that you know how to keep tests independent. Both are easy to write by hand, and both are easy to explain.

## Say it like this

"When I have the same check on many inputs, I use parametrize with a short table: a normal value, empty, both edges, and one invalid value. Each row runs as its own test, so a failure tells me which input broke. When tests need the same setup, I use a fixture so every test gets a fresh object and cannot affect the others. I keep the inputs and expected values in the test table so the reader sees them without searching."
