---
title: Monitoring and latency percentiles
summary: Track counts, error rate and tail latency (p50, p95, p99), because the mean hides slow requests.
tags: [production, monitoring]
---
```python
import math

def percentile(values, p):
    """Nearest-rank percentile, p from 0 to 100."""
    if not values:
        raise ValueError("no values")
    ordered = sorted(values)
    rank = max(1, math.ceil(p / 100 * len(ordered)))   # 1-based rank
    return ordered[rank - 1]

latencies = [12, 15, 11, 250, 14, 13, 16, 12, 900, 15]
percentile(latencies, 50), percentile(latencies, 95)   # (14, 900)
```

- Use it to describe latency, batch duration, score distributions and queue sizes.
- Key rule: sort, compute a rank, index. State which percentile definition you use.
- Say: "p95 is the value that 95% of requests are at or below. I watch the tail, not the mean."

<!-- more -->

## Details

For the list above the mean is 125.8 ms. No request took about 125 ms: eight were fast and two were very slow. The median says "typical is 14 ms" and p95 says "the tail is bad". Both are true and useful.

**Definitions differ.** Nearest rank returns a value that exists in the data. Interpolating methods return a point between two values:

```python
import statistics

sum(latencies) / len(latencies)                            # 125.8
statistics.quantiles(latencies, n=100, method="inclusive")[94]   # 607.5   interpolated p95
percentile(latencies, 100)                                 # 900   the maximum
percentile([7], 99)                                        # 7     one value is every percentile
```

In an interview, name the method and test the edges: empty input, one value, `p=0`, `p=100`.

**What to monitor for a model service** (four basics):

- Traffic: requests per minute.
- Errors: error rate and fallback rate.
- Latency: p50, p95, p99 per time window.
- Model health: share of missing features, score distribution, drift.

**Windows.** Compute percentiles per window (the last 5 minutes), not over all history, or a new problem is diluted by old data.

## Common mistakes

- Averaging percentiles of several servers or windows. The p95 of the whole is not the mean of the p95s. Merge the raw values or histograms.
- Reporting only the mean.
- Off-by-one between the 1-based rank and the 0-based index.
- Forgetting to sort, or sorting the caller's list in place.
- Leaving out failed or timed-out requests, which makes latency look better than it is.

## See also

- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- [Alerts, thresholds and hysteresis](#/kb/prod-drift-alerts-hysteresis)
- [Structured logging](#/kb/prod-structured-logging)
- [Health checks](#/kb/prod-health-checks)
