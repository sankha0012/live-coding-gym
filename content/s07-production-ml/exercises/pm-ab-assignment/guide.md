**Why this matters.** Every user must see the same variant on every request and server, without a database lookup. `random` fails this, and so does `hash()`, which changes between processes.

**How we get there.**
1. Validate first: no weights, a negative weight or a zero total is a `ValueError`.
2. Hash `f"{experiment}:{user_id}"` with `hashlib.sha256`. The digest is the same in every process, and the experiment name keeps experiments independent.
3. Turn the first 8 bytes into an integer and divide by `2**64`, giving a number in [0, 1). Multiply by the total weight to get a point on the weight line.
4. Walk the variants in dict order, adding weights to a running total, and return the first variant whose total passes the point.
5. Skip weight-0 variants so they never win; the last non-zero one is the safe fallback.

**Check it.** Work per call is proportional to the number of variants. Changing the weights later moves some users between variants.

**Watch out.** Hashing only `user_id` puts the same users in the same arm of every experiment, so results are secretly correlated.
