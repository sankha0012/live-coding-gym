A drift score (for example PSI) is computed every hour. If the alert fires and clears each time the score wobbles around one threshold, people stop trusting it. Write a class `DriftAlert(high: float, low: float)` with hysteresis.

- `update(score) -> str | None` feeds one new score and returns `"raised"` if the alert just turned on, `"cleared"` if it just turned off, and `None` if the state did not change.
- The attribute `active` is the current state. It starts as `False`.
- The alert is raised when the score is strictly above `high`.
- The alert is cleared when the score is strictly below `low`.
- Any score from `low` to `high` inclusive keeps the current state. A score above `high` while already active does nothing and returns `None`, and the same for a score below `low` while inactive.
- Raise `ValueError` if `low` is greater than `high`.
