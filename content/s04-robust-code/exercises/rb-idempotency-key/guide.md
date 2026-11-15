**Why this matters.** A payment request can arrive twice: the client retries after a timeout, or the queue redelivers it. If we run it twice, the customer is charged twice. The trick is to remember outcomes by request key, so the side effect happens once.

**How we get there.**
1. Keep a dict `_done` that maps each key to an outcome. The key identifies the request, so a repeat with a different payload is still the same request.
2. Check `if key not in self._done`. We use membership, not the stored value, because a real result can be `None` or `0`, and those must still count as done.
3. On a first sight, call `func(payload)` and store `(result, None)`. If it raises, store `(None, e)` instead, so failures are remembered too.
4. Finally read the outcome back. If there is an error, `raise` that same exception object; otherwise return the result.

**Check it.** A repeat calls `func` zero more times. Each call is constant time; memory grows with the number of keys.

**Watch out.** Testing the stored value for `None`, keying by payload, or forgetting failures all let a retry run the side effect again.
