---
title: "What to test: behaviours, edges, failure paths"
summary: "Pick tests by behaviour: one normal case, the edges that break code, and each way it should fail."
tags: [testing, pytest, edge-cases]
---
```python
import pytest

def mean(xs):
    if not xs:
        raise ValueError("empty input")
    return sum(xs) / len(xs)

def test_mean_of_several():    assert mean([1, 2, 3]) == 2     # normal behaviour
def test_mean_of_one_item():   assert mean([7]) == 7           # edge: one item
def test_mean_of_negatives():  assert mean([-2, 2]) == 0       # edge: sign
def test_mean_rejects_empty():                                 # failure path
    with pytest.raises(ValueError): mean([])
```

- Test what the code promises (input gives output), not how it does it inside.
- Minimum set: one normal case, one or two edges, one failure path.
- Decide the expected value before you run. Do not copy it from the output.

<!-- more -->

## Details

**Behaviours.** List the promises in the task statement. Each rule is one test: "ties go alphabetically", "returns at most k items", "ignores case". The test name says the rule, so a failure reads like a broken promise.

**Edges.** Pick the ones most likely to break this code:

| Shape of the problem | Edges worth a test |
|---|---|
| Lists and loops | empty, one item, all items equal |
| Counting and ranking | a tie, fewer items than asked for |
| Search | not found, first position, last position |
| Strings | empty, extra spaces, mixed case |
| Intervals | touching, one inside another |
| Numbers | zero, negative, very large, NaN |
| Limits and windows | just below, exactly at, just above |

**Failure paths.** For every `raise` and every guard in the code, write one test that triggers it. Guards are where bugs hide. Also test what happens when a dependency fails: a fake that raises once, a missing file, a missing key.

**Properties** help when the exact value is hard to know. The output has the same length as the input. The output is sorted. Running the function twice gives the same result. The input was not changed.

**Order of work in a live round.** First the tiny example from your plan. Then the single edge most likely to fail. Then say out loud what you did not test, and why it is safe or what you would add.

Do not test Python itself or a library. Test your own logic.

## Common mistakes

- Testing only the happy path.
- Asserting on private details such as the name of an internal dict. The test breaks on every refactor.
- Changing the expected value until the test passes, without checking it by hand.
- One giant test with ten asserts. The first failure hides the other nine.
- Comparing floats with `==`. Use `pytest.approx`.

## See also

- [pytest basics](#/kb/test-pytest-basics)
- [pytest.mark.parametrize](#/kb/test-parametrize)
- [Testing exceptions with pytest.raises](#/kb/test-raises)
- [The six-step live-coding routine](#/kb/iv-routine-six-steps)
