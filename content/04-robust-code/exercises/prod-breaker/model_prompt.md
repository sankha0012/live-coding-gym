Complete this CircuitBreaker class (Python, standard library only). [paste the skeleton]
call(fn, fallback):
- If open and clock() - opened_at < cooldown: return fallback without calling fn.
- Otherwise call fn. On success: reset failures to 0, close (opened_at = None), return the result.
- On any Exception: failures += 1 and return fallback. Open (opened_at = clock()) if failures >= max_failures,
  or if this was the trial call after a cooldown.
The clock is injected so tests don't sleep. Write a test with a fake clock covering: opening after N failures,
skipping calls while open, a successful trial after the cooldown, and a failed trial that re-opens it.
