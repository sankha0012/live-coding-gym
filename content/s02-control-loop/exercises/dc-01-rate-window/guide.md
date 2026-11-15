**Why this matters.** In the interview you are told the documentation can be consulted. Counting events in a window is easy to get wrong by one, and the only way to know which side of the interval is included is to read the reference.

**How we get there.**
1. Read `docs.md`. The signature is `window_slice(timestamps, start, end)`, and the window is `start <= t < end`.
2. The new request at `now` looks back `window` seconds, so `start = now - window` and `end = now`.
3. Because `end` is exclusive, a request made exactly at `now` is not counted, which matches the task. Because `start` is inclusive, a request exactly `window` seconds ago is counted.
4. The request is rejected when the count of recent events is `limit` or more, so compare with `>=`.

**Check it.** With `now=100`, `window=10`: an event at 90 counts, an event at 89 does not, an event at 100 does not.

**Watch out.** Widening `end` to `now + 1` or shifting `start` by one looks harmless but changes which boundary events are counted. Never guess a bound; the docs state it.
