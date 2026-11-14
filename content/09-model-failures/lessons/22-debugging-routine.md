# Debugging routine

## The problem it solves

In the live round you may get code that is wrong and a failing test. The risk is to guess, change three things and hope. A fixed routine keeps you calm and shows the interviewer how you think. The routine is: reproduce, shrink, hypothesise, check one thing at a time, then fix with the smallest safe change.

## The routine

1. **Reproduce.** Run the failing test and read the whole message. Do not change code yet.
2. **Shrink.** Reduce the failing input to the smallest one that still fails. One row, one date, one value.
3. **Hypothesise.** Say one sentence: "I think the window includes the end date when it should not."
4. **Check one thing.** Print or assert one value that proves or kills the guess. Change one thing at a time.
5. **Fix small.** Change the least that makes the test pass. Then run all tests again.
6. **Protect.** Add a test for the case you found.

## The smallest runnable example

A buggy function and the shrinking step.

```python
from datetime import datetime, timezone


def hours_between(a, b):
    return (b - a).total_seconds() / 3600


# Mixing naive and aware datetimes raises TypeError.
naive = datetime(2026, 1, 1, 12, 0)
aware = datetime(2026, 1, 1, 15, 0, tzinfo=timezone.utc)
try:
    hours_between(naive, aware)
except TypeError as e:
    print("reproduced:", e)

# Shrunk and fixed: make both sides UTC-aware.
fixed = naive.replace(tzinfo=timezone.utc)
assert hours_between(fixed, aware) == 3.0
print("ok")
```

The shrunk case is two datetimes. The hypothesis is "one is naive". The check is the error message. The fix is one line. The protecting test is the assert.

## Common bug shapes to guess first

- **Off by one:** a window with `<=` where `<` was meant. Test the exact boundary value.
- **Timezone:** naive and aware datetimes mixed, or local time near midnight. Convert to UTC at the edge.
- **Train-serve skew:** features are computed differently in training and serving, for example one fills missing with 0 and the other with the mean. Make both call the same function.
- **Mutation:** a function changes its input list, so the second call sees different data.

## Three traps people hit

1. **Changing several things at once.** If the test passes you do not know which change fixed it, and you may have added a new bug. One change, one run.
2. **Fixing the test, not the code.** If a test fails, first decide which side is wrong by reading the prompt. Change the test only when the stated requirement says it is wrong.
3. **Rewriting everything.** A large rewrite under time pressure creates new bugs. The smallest safe change is also the easiest to explain.

## What to say aloud

Narrate every step in short sentences. Silence looks like being lost, and a running commentary shows method even when you are slow.

## Say it like this

"First I run the test and read the error. It fails on one input, so I shrink it to a single row. My guess is that the boundary is inclusive when it should be exclusive. I print the one value that tests this guess. It confirms it, so I change one operator, run all tests, and add a test for the boundary so it cannot come back."
