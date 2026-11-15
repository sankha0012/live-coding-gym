---
title: Alerts, thresholds and hysteresis
summary: Turn an alert on at one threshold and off at a lower one, so a metric near the line does not flap.
tags: [production, monitoring, alerting]
---
```python
def alert_states(values, on_at, off_at):
    """On when a value reaches on_at; off only when it falls to off_at (off_at < on_at)."""
    firing, out = False, []
    for v in values:
        if not firing and v >= on_at:
            firing = True
        elif firing and v <= off_at:
            firing = False
        out.append(firing)
    return out

alert_states([0.10, 0.26, 0.24, 0.26, 0.14, 0.20], on_at=0.25, off_at=0.15)
# [False, True, True, True, False, False]
```

- Use it for drift scores, error rates, latency and any noisy metric with a threshold.
- Key rule: the alert is a small state machine. The next state depends on the value and on the current state.
- Say: "With one threshold a value that hovers near it fires and clears all day. Two thresholds stop that."

<!-- more -->

## Details

With a single threshold of 0.25, the series above would give on, off, on, off. Each change pages someone. Hysteresis keeps the alert on while the value sits in the band between `off_at` and `on_at`.

A second common tool is **persistence**: fire only after `n` breaches in a row. One noisy point is ignored.

```python
def breached_for(values, threshold, n):
    streak = 0
    for v in values:
        streak = streak + 1 if v > threshold else 0
        if streak >= n:
            return True
    return False

breached_for([0.3, 0.1, 0.3, 0.3], threshold=0.25, n=2)   # True
breached_for([0.3, 0.1, 0.3, 0.1], threshold=0.25, n=2)   # False
```

Other points to mention:

- **Severity levels.** For PSI a common reading is below 0.1 stable, 0.1 to 0.25 watch, above 0.25 act. Map levels to warn and page.
- **Missing data is a signal.** If the metric stops arriving, no threshold is crossed and the alert stays silent. Alert on "no data for N minutes" as well.
- **Enough samples.** A rate from 5 requests is noise. Require a minimum count per window.
- **Actionable.** Each alert should say what was measured, the value, the threshold and the window.

## Common mistakes

- A NaN metric: `nan >= 0.25` is False, so a broken pipeline never alerts. Check `math.isnan` first.
- Setting `off_at` equal to or above `on_at`, which removes the hysteresis.
- Forgetting to reset the streak when a value is back to normal.
- Mixing `>` and `>=` between the code and the written rule.
- Recomputing the state from the last value only, and losing the stored state between runs.

## See also

- [Drift and the population stability index (PSI)](#/kb/ml-psi-drift)
- [Monitoring and latency percentiles](#/kb/prod-monitoring-percentiles)
- [Floats, NaN, infinity and rounding](#/kb/py-math-nan)
