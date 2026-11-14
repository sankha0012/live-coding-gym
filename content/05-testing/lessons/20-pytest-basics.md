# Pytest basics

## The problem it solves

You write a function and run it once with one input. It works, so you move on. A week later someone changes it and a case you never checked breaks. A test is a small program that runs your function on chosen inputs and fails loudly when the answer is wrong. You write it once, and it checks the function every time after that.

Pytest is the standard tool in Python for this. It finds your tests, runs them, and shows what went wrong.

## The smallest runnable example

Put this in a file called `test_slug.py`:

```python
def slugify(text):
    return "-".join(text.lower().split())


def test_slugify_joins_words_with_dash():
    assert slugify("Hello World") == "hello-world"


def test_slugify_empty_string():
    assert slugify("") == ""


def test_slugify_extra_spaces():
    assert slugify("  a   b ") == "a-b"
```

Run it from the terminal with `uv run pytest -q`. Pytest collects every function whose name starts with `test_` in every file named `test_*.py`. Each one passes if it finishes without an error, and fails if an `assert` is false or any exception escapes.

In a real project the function lives in its own module, and the test file imports it: `from slug import slugify`. Here they share one file only to keep the example short.

## How assert works

Use the plain `assert` statement. You do not need `assertEqual` or other special methods. When an assert fails, pytest rewrites the message so it shows both sides:

```
>       assert slugify("A B") == "a_b"
E       AssertionError: assert 'a-b' == 'a_b'
E         - a_b
E         + a-b
E        +  where 'a-b' = slugify('A B')
```

That output tells you what the function returned, so you can fix it fast.

For floats, never compare with `==`. Use `pytest.approx`:

```python
import pytest


def test_mean_of_floats():
    assert sum([0.1, 0.2]) / 2 == pytest.approx(0.15)
```

`0.1 + 0.2` is not exactly `0.3` in binary floating point, so an exact compare can fail for no good reason. `approx` allows a tiny relative error.

## What a good test looks like

A good test has three parts, in this order: set up the input, call the function, assert the result. Keep it short and give it a name that says the behaviour: `test_slugify_empty_string`, not `test_1`. When it fails, the name alone should tell you what broke.

One test should check one behaviour. If a test has ten asserts for ten different ideas, the first failure hides the others and the name cannot describe it.

## Three traps people hit

1. **A test that cannot fail.** If you write `assert slugify("a b")` with no comparison, a non-empty string is always true, so the test always passes. Always compare to an exact expected value. A good habit: break the function on purpose once and check that the test goes red.
2. **Copying the code into the test.** If the test computes the expected value with the same logic as the function, a bug in the logic appears on both sides and cancels out. Write the expected value by hand from the specification: `== "hello-world"`.
3. **Forgetting the naming rule.** A function called `check_empty` or a file called `slug_tests.py` is silently ignored. Pytest says "no tests ran" or passes with fewer tests than you think. Look at the count in the summary line every time.

## Reading the result

A run ends with a summary such as `3 passed`. If something fails you see `F` in the progress line and a section for each failure with the line, the values, and the traceback. Run one test only with `uv run pytest test_slug.py::test_slugify_empty_string`. Stop at the first failure with `-x`. Show print output with `-s`.

## Why this matters in an interview

In a live coding round, a few well-chosen tests show that you think about correctness, not only about making the first example work. Writing the test first for the empty input and the odd input also tells the interviewer you know where bugs hide. It takes two minutes and it is easy to explain.

## Say it like this

"I write a small test for each behaviour in the prompt, using plain asserts and a name that says what it checks. I put in the normal case, the empty input and one odd input. I write the expected value by hand, not by reusing my own logic, and for floats I use approx. Then I run pytest and read the summary to make sure the number of tests is what I expect. If a test passes on the first try, I break the code on purpose to see it fail, so I know the test is real."
