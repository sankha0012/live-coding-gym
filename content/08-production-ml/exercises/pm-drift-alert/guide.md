**Why this matters.** If an alert has one threshold and the metric hovers around it, the alert turns on and off all night and people learn to ignore it. We use two thresholds and a remembered state, called hysteresis.

**How we get there.**
1. `low > high` raises `ValueError`; equal thresholds are allowed.
2. Store the thresholds and one boolean, `active`, starting at `False`.
3. When the alert is off, only a score strictly above `high` can turn it on: `if not self.active and score > self.high`. We set `active = True` and return `"raised"`.
4. When the alert is on, only a score strictly below `low` can turn it off: `if self.active and score < self.low`. We set it to `False` and return `"cleared"`.
5. Anything else returns `None`. Scores between the thresholds, including exactly `low` and `high`, change nothing, so the old state decides.

**Check it.** Because we test the state together with the threshold, a repeated high score while already active returns `None`, so the caller pages once.

**Watch out.** Checking only the score, such as `score > high` regardless of state, raises again on every high reading, and using `>=` breaks the boundary rule.
