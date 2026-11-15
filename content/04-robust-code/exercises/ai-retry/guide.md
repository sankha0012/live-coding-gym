**Why this matters.** A model API or tool call fails now and then for no good reason: a timeout, a busy server. A careless retry loop hammers the server or sleeps after the last failure for nothing.

**How we get there.**
1. Loop with `for attempt in range(max_tries)`: a counter and a hard limit in one.
2. Inside, `try: return fn()`. A success leaves at once.
3. On an exception, check whether this is the last attempt: `attempt == max_tries - 1`. If so, a bare `raise` re-raises the real error with its original traceback.
4. Otherwise wait `base * 2 ** attempt` seconds (1, 2, 4, ...) and loop again. Doubling gives the server room to recover.
5. Call the injected `sleep` instead of `time.sleep` directly, defaulting to `time.sleep` when none is given. Tests can then record the waits.

**Check it.** With 3 tries and all failing, we sleep twice (1 and 2 seconds), never after the third failure. Cost is at most `max_tries` calls.

**Watch out.** Sleeping before the final re-raise, or counting attempts from 1 so the waits come out as 2, 4, is the classic off-by-one here.
