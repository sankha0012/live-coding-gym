**Why this matters.** A timeout may work on the next try, but a bad request never will. Retrying everything wastes time, hammers the other service, and hides real bugs behind several slow failures.

**How we get there.**
1. Name the retryable errors once, in a tuple: `TimeoutError`, `ConnectionError` and `TransientError`.
2. Loop forever with an `attempt` counter, and `try: return fn()`. A success leaves at once.
3. Catch only that tuple. Anything else, such as `ValueError` or even `FileNotFoundError`, is not caught, so it flies out immediately with no sleep and no retry. That is why we do not write `except Exception` or `except OSError`.
4. In the handler, first check `attempt >= retries`. If so, a bare `raise` hands back the last transient error, before any sleep.
5. Otherwise `sleep(base_delay * 2 ** attempt)`, add one to `attempt`, and go round again. The delays are 1, 2, 4, ...

**Check it.** `fn` runs at most `retries + 1` times, and we sleep at most `retries` times. With `retries=0` it is one call and no sleep.

**Watch out.** Catching `OSError` or `Exception` retries permanent errors, and sleeping before the check pays a useless delay after the final failure.
