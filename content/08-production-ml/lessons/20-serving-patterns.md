# Serving patterns: batch, online, streaming

## The problem it solves

A model is only useful when its predictions reach a person or a system. How they get there is the serving pattern. If you pick the wrong one, you pay for servers you do not need, or users wait for answers that are hours old. In a live round the interviewer often asks "how would you serve this?" and wants a reason, not a buzzword.

There are three common patterns.

**Batch.** A scheduled job reads many rows, scores them all, and writes the results to a table or file. Nobody waits. Use it when predictions can be a few hours old: a nightly churn score, weekly restaurant rankings, a recommendation list built once a day. It is cheap and easy to retry.

**Online.** A service answers one request at a time, usually in tens of milliseconds, over HTTP or gRPC. Use it when the answer depends on data that exists only at request time: the items in this cart, the courier available right now. It needs low latency, autoscaling and good error handling.

**Streaming.** A consumer reads events from a queue such as Kafka and scores each one as it arrives, with seconds of delay. Use it when you react to events but no user waits on the reply: fraud flags, live delivery time updates, anomaly alerts.

A simple rule: start with batch. Move to online only when freshness or per-request inputs force you to.

## The smallest runnable example

The same scoring function can sit behind all three patterns. What changes is the loop around it.

```python
def score(row: dict) -> float:
    return min(1.0, row["distance_km"] / 10)

# Batch: score a whole table, write results once.
def run_batch(rows, write):
    write([{"id": r["id"], "score": score(r)} for r in rows])

# Online: one request, one answer, fail loudly on bad input.
def handle_request(payload: dict) -> dict:
    if "distance_km" not in payload:
        return {"error": "missing distance_km"}
    return {"score": score(payload)}

# Streaming: one event at a time from an iterator, never stop on one bad event.
def run_stream(events, emit):
    for e in events:
        try:
            emit({"id": e["id"], "score": score(e)})
        except (KeyError, TypeError):
            emit({"id": e.get("id"), "error": "bad event"})

out = []
run_batch([{"id": 1, "distance_km": 4}, {"id": 2, "distance_km": 30}], out.extend)
print(out)
print(handle_request({"distance_km": 5}))
run_stream([{"id": 3, "distance_km": 2}, {"id": 4}], print)
```

Notice that the scoring logic is written once and tested once. The wrappers differ only in how they handle failure. Batch can retry the whole job. Online must answer inside a time limit. Streaming must keep going.

## The three traps

**1. Training-serving skew.** The features are computed one way in the training notebook and another way in the service. The model looks fine offline and bad in production. The fix is to share one feature function between training and serving, and to compare online values with offline values on a sample.

**2. Choosing online because it feels modern.** An online service needs on-call, autoscaling and latency budgets. If the business only reads the scores each morning, a nightly batch is cheaper, simpler and easier to reproduce. Always ask "how old can the answer be?" before you choose.

**3. No plan for the slow or broken model.** In an online path, one slow model call can block every request behind it. Set a timeout, return a fallback value such as a global average or the last known score, and count how often the fallback fires. In a streaming path, one poison message that raises an exception can stop the consumer. Catch it, send the event to a dead-letter queue, and move on. In batch, make the job resumable: write progress so a crash at row 900,000 does not restart from row 1.

A fourth point worth a sentence: all three patterns need idempotence. If the same batch runs twice or the same event arrives twice, the result should be the same, not duplicated rows.

## Which one for which question

| Question | Pattern |
| --- | --- |
| Can the score be a day old? | Batch |
| Does it need data from this exact request? | Online |
| Does it react to events with no user waiting? | Streaming |
| Do you need both a nightly refresh and a live check? | Batch plus online, sharing one feature function |

Many real systems mix them. A batch job precomputes heavy features. The online service reads them and adds the request-time ones.

## Say it like this

"I would start by asking how fresh the prediction has to be. If a daily answer is fine, I run a batch job, because it is cheap and easy to retry and backfill. If the input only exists at request time, I serve online with a timeout and a fallback. If we react to events without a waiting user, I use a stream with a dead-letter queue for bad events. In every case I keep one feature function for training and serving to avoid skew, and I make the work idempotent so a retry does not duplicate results."
