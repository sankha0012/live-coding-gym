# Monitoring basics

## The problem it solves

A deployed model fails quietly. The service stays up and returns numbers, but the numbers get worse because the world changed. Without monitoring you find out from an angry stakeholder weeks later. Monitoring gives you three things: an early warning, a way to find the cause, and proof that a fix worked.

## What to log

For every prediction, log enough to replay it later:

- a request id and a timestamp
- the model name and version
- the input features, or a hash of them if they are sensitive
- the prediction, and the score or confidence
- the latency, and whether a fallback was used
- the true label when it arrives later, joined by request id

Log as structured data, one JSON object per line. Free text is hard to query.

## Latency percentiles

The average hides the slow requests that users feel. Report percentiles: p50 is the typical request, p95 and p99 are the tail. If p50 is 40 ms and p99 is 2 s, one request in a hundred is painful even though the average looks fine.

The nearest-rank method is simple: sort the values, then take the item at position `ceil(p/100 * n)`, counting from 1.

```python
import math

def percentile(values, p):
    if not values:
        raise ValueError("no values")
    ordered = sorted(values)
    rank = math.ceil(p / 100 * len(ordered))
    return ordered[max(rank, 1) - 1]

latencies = [20, 22, 25, 30, 31, 35, 40, 45, 300, 2000]
print(percentile(latencies, 50), percentile(latencies, 95), percentile(latencies, 99))
print(sum(latencies) / len(latencies))
```

The mean is 254.8 ms, which describes nobody. The p50 is 31 ms and the p99 is 2000 ms, which tells the real story.

## Data drift and prediction drift

**Data drift** means the inputs changed: a new city, a new app version that sends distances in meters, a null rate that jumped. **Prediction drift** means the model outputs changed shape: suddenly most scores are above 0.9. Neither needs labels, so you can watch both in real time. **Concept drift** means the link between inputs and the label changed. That needs labels, so it shows up late.

A common drift number is the Population Stability Index (PSI). Bin the training values, compare the share in each bin with the share in live data, and sum `(live - train) * ln(live / train)`.

```python
import math

def psi(expected, actual, eps=1e-6):
    total = 0.0
    for e, a in zip(expected, actual):
        e, a = max(e, eps), max(a, eps)
        total += (a - e) * math.log(a / e)
    return total

train_share = [0.25, 0.25, 0.25, 0.25]
live_share = [0.10, 0.20, 0.30, 0.40]
print(round(psi(train_share, live_share), 3))
```

A rule of thumb: below 0.1 is stable, 0.1 to 0.25 deserves a look, above 0.25 is a large shift. These are conventions, not laws. Check them against your own data.

## Alert thresholds

An alert should be something a person can act on. Page for things that hurt users now: error rate, p99 latency, a missing data feed. Send a ticket for slow things: mild drift, a falling accuracy trend. Set thresholds from real history, not from a guess.

## The three traps

**1. Alert flapping.** A metric hovering around the threshold fires, clears, and fires again all night. People then ignore the alerts. Use hysteresis: raise the alert above 0.25, but clear it only when the value falls below 0.20. Or require the breach to last for several windows.

**2. Watching only the average.** A mean latency or mean score can stay flat while one segment, such as one city or one app version, breaks. Slice the key metrics by the segments that matter.

**3. Monitoring only the model, not the data going in.** Most production incidents are upstream: a column renamed, a feed that went empty, a unit change. Check null rates, ranges and row counts on the input first. They are cheap and they catch the common failure.

One more habit: when labels arrive late, track a proxy meanwhile, such as the score distribution, and compute real precision and recall once labels land.

## Say it like this

"I log every prediction with the model version, features, score, latency and a request id, so I can replay any case. I watch p50, p95 and p99 latency, not the mean, because the tail is what users feel. I track data drift on inputs and prediction drift on outputs, for example with PSI, since both work without labels. I set thresholds from history and add hysteresis so alerts do not flap. And I check input quality first, because most incidents come from the data, not the model."
