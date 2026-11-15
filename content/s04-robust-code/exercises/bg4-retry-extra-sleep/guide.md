**Why this matters.** Retry code runs when something is already wrong. An extra wait in that path adds latency exactly when the caller can least afford it.

**How we get there.**
1. Run the tests. Four fail, and every failing test is about a call that never succeeds.
2. Reproduce: `fn` always raises `TimeoutError`, `retries=2`, and `sleep=sleeps.append`. The list is `[1.0, 2.0, 4.0]`, but the rule says at most two sleeps: `[1.0, 2.0]`.
3. Read the loop. `for attempt in range(retries + 1)` makes three attempts, which is right.
4. Look at where `sleep` is called: inside `except`, directly after storing the error, with no check on whether this was the last attempt.
5. Fix it: in the `except` block, `if attempt == retries: raise`, otherwise sleep. Run the tests again.

**Check it.** The successful paths were already passing, which is why this bug survives a quick manual test. The failing paths are the ones to run.

**Next time.** With AI-written retry code, always test the case where every attempt fails and count the sleeps.

**Watch out.** Removing the `last` variable and re-raising is fine, but make sure the last error, not the first, is the one raised.
