**Why this matters.** When we roll out a new model to a small share of users, each user must stay on the same side on every request and every server. Random choice or Python's `hash()` would flip people between models.

**How we get there.**
1. Build a stable text from the inputs: `f"{salt}:{user_id}"`. The salt lets us reshuffle for the next rollout.
2. Hash it with `hashlib.sha256`. Unlike `hash()`, the result is the same in every process and on every day.
3. Convert the hex digest to an integer with `int(digest, 16)`, and take `% 100`. That gives each user a fixed bucket from 0 to 99.
4. Return `"canary"` if `bucket < canary_percent`, otherwise `"stable"`.

**Check it.** At 0 no bucket is below 0, and at 100 every bucket is below 100, so the extremes work without special code. Raising the percent only adds buckets, so no one leaves the canary mid-rollout. The share is only approximate on small samples.

**Watch out.** Using `random` or `hash()` looks fine in a quick test but breaks stickiness across servers and restarts, and using `<=` instead of `<` gives one extra percent.
