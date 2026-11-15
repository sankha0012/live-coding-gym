# Batch, online and streaming serving

## What it is

A serving pattern is how predictions reach whoever uses them. In batch serving a scheduled job scores many rows and writes the results to a table. In online serving a service answers one request at a time, usually in tens of milliseconds. In streaming serving a consumer reads events from a queue and scores each one within seconds, with no user waiting for the reply. The scoring logic is the same in all three; the loop around it and the way it handles failure differ. The choice starts with one question: how old may the answer be? See [train-serve skew](#/kb/prod-train-serve-skew) for the main risk when two paths share a model.

## How it breaks in production

Batch breaks by size and repetition. A job that crashes at row 900,000 restarts from zero, and a job that runs twice appends duplicate rows. Online breaks by tail latency: one slow dependency blocks every request behind it, and a malformed payload that raises an exception returns a stack trace instead of a clean error. Streaming breaks on poison events: a single bad message that raises inside the consumer loop stops the whole stream, and at-least-once delivery means the same event can arrive twice.

## The defence in code

```python
def score(row: dict) -> float:
    return min(1.0, row["distance_km"] / 10)

def run_batch(rows):
    return {r["id"]: score(r) for r in rows}      # keyed by id: a rerun overwrites, never duplicates

def handle_request(payload: dict) -> dict:
    if not isinstance(payload.get("distance_km"), (int, float)):
        return {"status": 422, "error": "distance_km must be a number"}
    return {"status": 200, "score": score(payload)}

def run_stream(events, emit, dead_letter):
    for e in events:
        try:
            emit(e["id"], score(e))
        except (KeyError, TypeError):
            dead_letter.append(e)                 # park the bad event and keep going

print(run_batch([{"id": 1, "distance_km": 4}, {"id": 2, "distance_km": 30}]))
print(handle_request({"distance_km": "far"}))
out, dlq = {}, []
run_stream([{"id": 3, "distance_km": 2}, {"id": 4}], out.__setitem__, dlq)
print(out, dlq)
```

The batch result is keyed by id, so it is idempotent. The handler validates first. The stream parks the bad event instead of dying.

## What to say in the interview

"I start by asking how fresh the prediction has to be. If a daily answer is fine I run a batch job, because it is cheap, easy to retry and easy to reproduce. I go online only when the input exists only at request time, and then I add validation, a timeout and a fallback. For event-driven work I use a stream with a dead-letter queue. In every case I share one feature function between training and serving and keep the work idempotent."
