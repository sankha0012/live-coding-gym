# Partial batch failure

## What it is

A batch job scores many rows. Partial batch failure is what happens when a few of them are bad, with a missing field, a wrong type or a value that makes the model raise, and the job has to decide what to do about the rest. The naive loop lets the first exception kill the whole run. See [chunked batch processing](#/kb/prod-chunked-batch-processing).

## How it breaks in production

A nightly job scores two million customers. Row 1,200,000 has a malformed date, the exception propagates, and the job dies. Nothing is written, or only half of it is, and the morning reports are empty or inconsistent. The opposite mistake is just as bad: wrapping everything in a bare `except: pass` hides bad rows completely, so a broken upstream feed produces 30 percent missing scores and nobody learns about it. The right behaviour is isolation plus visibility: bad rows are set aside with a reason, good rows proceed, and the failure rate is reported and checked against a limit.

## The defence in code

Wrap the per-row work, collect the failures, and fail the whole job only if too many rows failed. Rerunning must be safe, so write results by row id rather than appending blindly (see [idempotency](#/kb/prod-idempotency)).

```python
def score_batch(rows, score_fn, max_failure_rate=0.2):
    results, failures = {}, []
    for row in rows:
        try:
            results[row["id"]] = score_fn(row)
        except Exception as exc:
            failures.append((row.get("id"), type(exc).__name__))
    rate = len(failures) / len(rows) if rows else 0.0
    if rate > max_failure_rate:
        raise RuntimeError(f"failure rate {rate:.0%} above limit")
    return results, failures

rows = [{"id": 1, "x": 2}, {"id": 2}, {"id": 3, "x": 4}, {"id": 4, "x": 1},
        {"id": 5, "x": 3}, {"id": 6, "x": 0}]
results, failures = score_batch(rows, lambda r: r["x"] * 0.1)
assert results == {1: 0.2, 3: 0.4, 4: 0.1, 5: 0.30000000000000004, 6: 0.0}
assert failures == [(2, "KeyError")]

try:
    score_batch(rows, lambda r: r["missing"])
except RuntimeError as e:
    print("job failed:", e)
```

Catching `Exception` at the row boundary, not a bare `except:`, lets real interpreter exits such as KeyboardInterrupt through.

## What to say in the interview

"I isolate failures per row: a bad row is recorded with its id and the error type, and the good rows still get processed. I then check the failure rate against a limit and fail the job loudly if it is exceeded, because a high rate means the upstream data is broken, not that a few rows are odd. I would write results by id so a rerun is idempotent and does not duplicate output."
