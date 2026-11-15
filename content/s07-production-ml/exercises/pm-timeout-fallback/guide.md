**Why this matters.** A real-time service has to answer in time, even when the model is slow or broken. A late answer is as bad as none, so we fall back to a safe default and report which path we took.

**How we get there.**
1. Read the injected clock before the call: `start = clock()`. Never the real clock.
2. Call `model(x)` once inside `try`, and catch `Exception`. On failure, return `(fallback, "error")` straight away, with no retry. We catch `Exception` and not `BaseException`, so Ctrl+C still works.
3. Read the clock again and compare `clock() - start > deadline_s`. If so, the result is too old to use, so return `(fallback, "timeout")`.
4. Otherwise return `(result, "model")`. We do not test the result for truth, so `0` and `None` are valid answers.

**Check it.** Taking exactly `deadline_s` is still on time, which is why the test is `>` and not `>=`. A model that is slow and raises counts as an error, since the exception comes first. The path label lets us count each case.

**Watch out.** This check runs after the call, so it cannot interrupt a call that hangs for ever; that needs a real timeout.
