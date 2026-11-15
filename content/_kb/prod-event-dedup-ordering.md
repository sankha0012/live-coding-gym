---
title: Duplicate and out-of-order events
summary: Skip events already seen by id, and let only a newer event overwrite the state for a key.
tags: [production, streaming]
---
```python
def dedupe(events, seen):
    for e in events:
        if e["id"] not in seen:         # at-least-once delivery: drop repeats
            seen.add(e["id"])
            yield e

def upsert(state, key, value, version):
    old = state.get(key)
    if old is None or version > old[1]: # an older event never overwrites a newer one
        state[key] = (value, version)
```

- Use it for any consumer of a queue or stream: feature updates, status changes, counters.
- Key rule: identity comes from the event id, order comes from the event time, never from arrival order.
- Say: "Queues deliver at least once and not in order, so I dedupe by id and keep the latest by event time."

<!-- more -->

## Details

```python
events = [
    {"id": "e2", "sensor": "s1", "ts": 20, "temp": 21.5},
    {"id": "e1", "sensor": "s1", "ts": 10, "temp": 19.0},   # arrives late
    {"id": "e2", "sensor": "s1", "ts": 20, "temp": 21.5},   # delivered twice
]
state, seen = {}, set()
for e in dedupe(events, seen):
    upsert(state, e["sensor"], e["temp"], (e["ts"], e["id"]))
state          # {'s1': (21.5, (20, 'e2'))}
len(seen)      # 2
```

The late event `e1` is processed but does not replace the newer value. The second `e2` is dropped.

**Two times.** Event time is when it happened. Arrival time is when you received it. State must follow event time.

**Ties.** Two different events can have the same timestamp. Make the version a tuple such as `(ts, id)` so there is always one winner and the result does not depend on arrival order.

**Counters and sums.** "Latest wins" is enough for a status. For a sum, a duplicate adds twice, so the dedupe step is what keeps it correct.

**Batch versus stream.** In a batch you can sort by `(ts, id)` and then apply. In a stream you cannot wait forever, so you choose how late an event may be (a watermark) and drop or side-log anything later.

**Memory.** The `seen` set grows without limit. Keep ids only for a time window longer than the possible redelivery delay.

## Common mistakes

- Deduplicating on the payload or the key instead of the event id. Two real events can look the same.
- Assuming the input is sorted because the test data happened to be.
- Comparing with `>=`, so a duplicate or an equal-time event overwrites and the result depends on arrival order.
- Comparing timestamps as strings in mixed formats, or mixing naive and aware datetimes.
- Marking an id as seen before its processing succeeded, so a failed event is never retried.

## See also

- [Idempotency and idempotency keys](#/kb/prod-idempotency)
- [Sets and set operations](#/kb/py-sets)
- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- [Dates and times: datetime, timedelta, zoneinfo](#/kb/py-datetime)
