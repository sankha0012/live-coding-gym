# What to test

## The problem it solves

Knowing the syntax of pytest is the easy part. The real skill is choosing the checks. Too few tests miss bugs. Too many tests, all of the same kind, give false confidence and are slow to read. In an interview you have a few minutes, so you must pick the tests that catch the most bugs.

A simple rule: test behaviours, then edges, then failure paths.

## The smallest runnable example

Take a function that splits a list into batches of a given size:

```python
import pytest


def batch_split(items, size):
    if size <= 0:
        raise ValueError("size must be positive")
    return [items[i:i + size] for i in range(0, len(items), size)]


# behaviour: the normal case, order kept
def test_splits_in_order():
    assert batch_split([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]


# edges
def test_last_batch_is_smaller():
    assert batch_split([1, 2, 3], 2) == [[1, 2], [3]]


def test_empty_input():
    assert batch_split([], 3) == []


def test_size_larger_than_input():
    assert batch_split([1, 2], 5) == [[1, 2]]


# failure paths
@pytest.mark.parametrize("bad", [0, -1])
def test_rejects_non_positive_size(bad):
    with pytest.raises(ValueError):
        batch_split([1], bad)


# does not change its input
def test_input_is_not_modified():
    data = [1, 2, 3]
    batch_split(data, 2)
    assert data == [1, 2, 3]
```

Six checks, under a minute to write, and each one names a different idea.

## The three groups

**Behaviours.** What the prompt says the function does. One test per sentence of the specification. If the prompt says "keep the first occurrence and the original order", that is two tests.

**Edges.** The places where code switches between branches. Empty input. One item. Exactly at the limit. One below and one above the limit. Duplicates. Negative or zero. A value that is the same everywhere, such as a constant column when you scale data, where dividing by the range gives zero over zero. Missing values and `None` when the prompt allows them.

**Failure paths.** What happens on bad input or a failing dependency. Which exception, with which message. What state is left behind: is the input untouched, is the balance unchanged after a refused withdrawal, are partial results thrown away.

For code in ML systems, add the property checks: same input gives the same output (determinism), running twice does not change the result (idempotency), and output has the expected shape and range, for example probabilities between 0 and 1.

## How many tests is enough

There is no magic number. A useful answer is: one test per behaviour sentence, one per edge in the code, one per failure path you chose to handle. For a small function that is usually four to eight tests. Stop when a new test would only repeat an idea you already cover. Coverage numbers can show lines that never ran, but a line that ran is not a line that was checked.

A good way to check yourself is to ask: if I made one small mistake in this function, would a test go red? Think of off-by-one in a slice, `<` instead of `<=`, a forgotten `sort`, a mutated argument. If you can name a mistake no test would catch, add a test for it.

## Three traps people hit

1. **Only the happy path.** Three tests with normal inputs pass for code that crashes on an empty list. Always add empty, one item, and one bad value.
2. **Testing the implementation, not the behaviour.** A test that checks which helper was called breaks when you refactor, even if the result is the same. Check inputs and outputs, not internal steps.
3. **Tests that depend on each other or on luck.** A test that needs another one to run first, uses the real clock, or draws unseeded random numbers fails at random. Make every test independent and deterministic, with fixed seeds and injected time.

## Why this matters in an interview

The interviewer watches how you decide what to check. Saying "behaviours, edges, failures" out loud, and then writing a short parametrized table, shows a clear method. It also shows you understand the usual failures of ML code: empty batches, constant features, missing values, and flaky services.

## Say it like this

"I choose tests in three groups. First the behaviours in the prompt, one test each. Then the edges: empty, one item, the exact limit, duplicates, and a constant input. Then the failure paths: which error is raised and that the input and state are unchanged. For this size of function that is about six tests. To check I have enough, I imagine small mistakes, like an off-by-one or a forgotten sort, and make sure at least one test would fail for each. I keep the tests deterministic by seeding randomness and injecting the clock."
