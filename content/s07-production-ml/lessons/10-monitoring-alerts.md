# Monitoring and alerts

## What it is

Monitoring means watching a deployed model with numbers you can act on. There are two layers. Service health covers request rate, error rate and latency. Model health covers data drift (the inputs changed), prediction drift (the output distribution changed) and real performance once labels arrive. An alert is a rule that turns a number into a message to a person, with a threshold, a duration and an owner. See [PSI drift](#/kb/ml-psi-drift), [drift alerts with hysteresis](#/kb/prod-drift-alerts-hysteresis) and [structured logging](#/kb/prod-structured-logging).

## How it breaks in production

A model fails quietly: the service stays up and returns numbers, but they are wrong because the data changed. Labels arrive late, so accuracy is not available for days, and drift is the only early signal. Alerts have their own failure modes. A metric that hovers around the threshold fires, clears and fires again all night, a flapping alert, and people learn to ignore it. A mean can stay flat while one city or one app version breaks, so unsliced metrics hide incidents. A drift score of 0.3 does not prove the model is wrong; it says to look closer.

## The defence in code

```python
import math

def psi(expected, actual, eps=1e-6):
    total = 0.0
    for e, a in zip(expected, actual):
        e, a = max(e, eps), max(a, eps)         # avoid log(0)
        total += (a - e) * math.log(a / e)
    return total

class Alert:
    def __init__(self, raise_at: float, clear_at: float):
        self.raise_at, self.clear_at, self.firing = raise_at, clear_at, False

    def update(self, value: float) -> bool:
        if not self.firing and value > self.raise_at:
            self.firing = True
        elif self.firing and value < self.clear_at:
            self.firing = False                 # clears only well below the raise level
        return self.firing

train = [0.25, 0.25, 0.25, 0.25]
live = [0.10, 0.20, 0.30, 0.40]
print(round(psi(train, live), 3))

alert = Alert(raise_at=0.25, clear_at=0.20)
print([alert.update(v) for v in [0.20, 0.26, 0.24, 0.26, 0.19]])
```

PSI compares the share of rows per bin. The rule of thumb is below 0.1 stable and above 0.25 a large shift; check it against your own history. The alert fires at 0.26, stays on at 0.24, and clears only at 0.19.

## What to say in the interview

"I watch service metrics, which are p99 latency and error rate, and model metrics, which are input drift, prediction drift and quality once labels arrive. I slice by the segments that matter, and I check input quality first because most incidents come from the data. Alerts have a threshold from real history, a duration, hysteresis so they do not flap, and an owner. I page for what hurts users now and open a ticket for slow trends."
