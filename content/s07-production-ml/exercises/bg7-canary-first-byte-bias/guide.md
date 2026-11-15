**Why this matters.** A canary that gets the wrong share of traffic makes the rollout size and the metrics comparison unreliable, and nothing crashes to tell you.

**How we get there.**
1. Run the tests. The three share tests fail with roughly 6 percent at a 5 percent canary and roughly 58 percent at 50 percent. Stability and salt tests pass.
2. Reproduce: `sum(assign_arm(str(i)) == "canary" for i in range(100_000)) / 100_000`. It is clearly above 0.05.
3. Read the bucket line. `digest[0]` is one byte, so a value from 0 to 255, and `% 100` maps 256 values onto 100 buckets unevenly (0 to 55 get three values, 56 to 99 get two).
4. Fix: use the whole digest, `int(hashlib.sha256(...).hexdigest(), 16) % 100`. A 256-bit number makes the remaining unevenness vanishingly small.

**Check it.** Rerun the share tests, and check monotonic growth: whoever is in at 5 percent is still in at 10.

**Watch out.** Changing the hashing for live users reshuffles who is in the canary, so do it before the rollout or with a new salt.
