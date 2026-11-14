You are rolling out a new model to about 5 percent of users. Write `assign_arm(user_id: str, canary_percent: int = 5, salt: str = "canary-v1") -> str` that returns `"canary"` or `"stable"`.

- The same user must always get the same arm, in any process and on any day. Do not use `random` and do not use the built-in `hash()` of a string, because it changes between runs. Use `hashlib`.
- Hash the text `f"{salt}:{user_id}"`, turn the digest into an integer, and take it modulo 100 to get a bucket from 0 to 99. A user is in the canary when their bucket is below `canary_percent`.
- `canary_percent=0` sends everyone to `"stable"`. `canary_percent=100` sends everyone to `"canary"`.
- Raising the percent only adds users: anyone in the canary at 5 percent is still in the canary at 10 percent.
- A different `salt` must reshuffle which users land in the canary.
- Over many ids the canary share must be close to `canary_percent`.
