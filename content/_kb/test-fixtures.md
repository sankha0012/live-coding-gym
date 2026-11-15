---
title: Fixtures and tmp_path
summary: A fixture builds what a test needs; a test asks for it by parameter name. tmp_path is a fresh temp folder.
tags: [testing, pytest, fixtures]
---
```python
import pytest

@pytest.fixture
def users():                       # runs again for every test that asks for it
    return [{"name": "ana"}, {"name": "bo"}]
def test_count(users):             # ask by naming it as a parameter
    assert len(users) == 2

def test_write_file(tmp_path):     # built-in: a new empty pathlib.Path folder
    f = tmp_path / "out.txt"
    f.write_text("hi")
    assert f.read_text() == "hi"
```

- A fixture is a function with `@pytest.fixture`. pytest calls it and passes the result to the test.
- By default each test gets a fresh result, so tests cannot affect each other.
- Use `tmp_path` for any test that reads or writes files. Never write into the project folder.

<!-- more -->

## Details

**Setup and teardown.** Use `yield` in place of `return`. The code after `yield` runs when the test ends, even if it failed:

```python
@pytest.fixture
def log():
    events = ["open"]
    yield events                   # the test runs here
    events.append("close")         # teardown

def test_log_starts_open(log):
    assert log == ["open"]
```

**Fixtures can use fixtures.** Name the other fixture as a parameter:

```python
@pytest.fixture
def data_file(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("id,amount\n1,10\n")
    return p

def test_reads_two_lines(data_file):
    assert len(data_file.read_text().splitlines()) == 2
```

**Scope.** `@pytest.fixture(scope="module")` builds the value once per file, and `scope="session"` once per run. Use that only for slow, read-only things.

**Sharing.** Fixtures in a file named `conftest.py` are available to every test in that folder, with no import.

Other built-in fixtures: `monkeypatch` replaces attributes and environment variables, and `capsys` captures printed output:

```python
def test_prints_hello(capsys):
    print("hello")
    assert capsys.readouterr().out == "hello\n"
```

## Common mistakes

- Calling the fixture yourself, as in `users()`. Name it as a parameter and let pytest call it.
- Forgetting the `@pytest.fixture` decorator. pytest then reports `fixture 'users' not found`.
- A module-scoped fixture that returns a list which one test changes. Later tests see the change.
- Treating `tmp_path` as a string. It is a `pathlib.Path`. Use `/` to join and `str(tmp_path)` if a function needs text.
- Writing test files with a fixed name in the current folder, which leaves rubbish behind and breaks parallel runs.

## See also

- [pytest basics](#/kb/test-pytest-basics)
- [Fakes, fake clocks and monkeypatch](#/kb/test-fakes-monkeypatch)
- [Files and pathlib](#/kb/py-files-pathlib)
- Official docs: https://docs.pytest.org/
