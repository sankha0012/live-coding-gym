**Why this matters.** A token bucket protects an API from a client sending too many calls. It allows short bursts but caps the long-run rate, and it needs no background thread: it works out what it earned only when asked.

**How we get there.**
1. Reject `capacity <= 0` or `refill_per_s <= 0` with `ValueError`. Start with `tokens = float(capacity)`, a full bucket, and remember `last = clock()`.
2. In `allow`, read the clock once and compute `elapsed = max(0.0, now - self.last)`. The `max` means a clock that goes backwards adds nothing and loses nothing.
3. Set `self.last = now`, so the next refill is measured from this call, even if time moved backwards.
4. Add `elapsed * rate` to the tokens and cap with `min(self.capacity, ...)`, so an idle client cannot save up an unlimited burst.
5. If `cost > self.tokens`, return `False` and take nothing. Otherwise subtract the cost and return `True`. A cost above capacity can never pass this check.

**Check it.** Each call is constant time and memory.

**Watch out.** Subtracting before checking lets a denied call eat tokens, and skipping the `min` cap or the `max(0, ...)` guard breaks the bucket after idle time or a clock jump.
