**Why this matters.** A model can go stale because it is old, or because the data it learned from is old. A model retrained yesterday on year-old data is still stale, so we check both ages.

**How we get there.**
1. Take `now` as a parameter rather than reading the clock. The answer then depends only on the inputs, which makes it predictable.
2. Reject impossible input: if `trained_at` or `data_end` is after `now`, raise `ValueError`. A negative age means a broken clock or bad metadata, and we should not report it as fresh.
3. Subtract the datetimes to get a `timedelta`, and convert it with `total_seconds() / 86400`. This keeps the fraction of a day.
4. Compare each age with its limit using strict `>`. Both flags are computed independently and returned with the two ages.

**Check it.** An age exactly equal to the limit is not stale. The work is constant.

**Watch out.** `timedelta.days` throws away the fraction, so 7.5 days becomes 7 and a stale model passes. Using `>=` flags a model at exactly its limit.
