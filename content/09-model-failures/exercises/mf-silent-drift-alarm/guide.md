**Why this matters.** Drift raises no error: the inputs just change and predictions get worse. We compare a live window with a reference window, in units of the reference's own spread.

**How we get there.**
1. Handle empty windows first: return `no_data` with no alarm. A monitor that crashes is worse than one that is briefly quiet.
2. Compute the reference spread once with `pstdev`, the population version, and set `limit = k * rs`. Both checks use this limit.
3. Mean check: if `abs(mean(live) - mean(reference)) > limit`, add `"mean"`.
4. Spread check: if `abs(pstdev(live) - rs) > limit`, add `"std"`. The absolute value matters, or a shrinking spread never alarms.
5. Return `alarm` as `bool(reasons)`, with reasons in the order added.

**Check it.** If `rs` is 0 the limit is 0, so any change counts, and a value exactly on the limit does not. Cost is linear.

**Watch out.** The sample standard deviation changes the limit, and checking only the mean misses a feature that spreads out or collapses.
