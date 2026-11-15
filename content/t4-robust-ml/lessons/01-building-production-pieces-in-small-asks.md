# Building production-style pieces in small asks

## The problem it solves

Retry logic, rate limiters, caches, drift alerts and batch checkpoints are the kind of thing an assistant can write in seconds, and also the kind of thing where a subtle bug costs a lot. Each piece has a few rules that you must know and check. Your job is to hold the rules, split the work into small asks and verify each against them.

## The method

1. **Write the contract first** as comments: inputs, outputs, and the rules that must hold.
2. **Split into functions** of a few lines each: parse, decide, act.
3. **Ask for one function at a time**, with an example.
4. **Test the rules**, not only the example: one assert per rule.
5. **Separate time and randomness** from the logic: pass a clock or a seed in, so tests are exact.
6. **Keep one hand change** per piece, such as the boundary or a default.

## Example: a retry decision

Contract (as comments):

```python
# retry only on errors that are temporary (timeout, 503), not on bad input (400)
# wait base * 2**attempt seconds between attempts, never more than a cap
# stop after max_attempts and raise the last error
```

Small asks, one per rule:

1. "Write `is_retryable(status)` returning `True` for 429, 500, 502, 503 and 504, `False` otherwise."
2. "Write `delay(attempt, base, cap)` returning `min(cap, base * 2 ** attempt)`."
3. "Write `call_with_retry(fn, max_attempts, sleep)` that uses those two functions; `sleep` is passed in."

Passing `sleep` in lets a test record the waits instead of waiting:

```python
waits = []
assert delay(0, 1, 10) == 1
assert delay(5, 1, 10) == 10      # capped
```

What to check in the assistant's version: no retry on non-retryable errors, the loop makes exactly `max_attempts` attempts, the last error is raised and not swallowed, and the delay does not grow without a cap.

## Rules to hold for each family

- **Retries and timeouts**: retry only temporary failures; back off; cap the wait; set a deadline; make the operation safe to repeat (see idempotency). [Retry with backoff](#/kb/prod-retry-backoff), [Timeouts](#/kb/prod-timeouts-deadlines), [Idempotency](#/kb/prod-idempotency).
- **Rate limits and caches**: inject the clock; decide what happens at the boundary (exactly at the limit, exactly at expiry). [Token bucket](#/kb/prod-rate-limiter-token-bucket), [TTL cache](#/kb/prod-ttl-cache), [Clock injection](#/kb/py-time-clock-injection).
- **Streams and batches**: process in chunks, never load everything; checkpoint progress so a restart resumes; handle duplicates and late events. [Chunked processing](#/kb/prod-chunked-batch-processing), [Checkpointing](#/kb/prod-checkpointing), [Event dedup and ordering](#/kb/prod-event-dedup-ordering).
- **Inputs and config**: validate at the edge, fail with a clear message, version the schema. [Input validation](#/kb/prod-input-validation), [Schema evolution](#/kb/prod-schema-evolution).
- **Monitoring**: percentiles instead of averages for latency; alerts that avoid flapping. [Percentiles](#/kb/prod-monitoring-percentiles), [Drift alerts with hysteresis](#/kb/prod-drift-alerts-hysteresis), [PSI drift](#/kb/ml-psi-drift).
- **Rollouts**: split traffic deterministically, with a fallback ready. [Canary, shadow and A/B](#/kb/prod-canary-shadow-ab), [Fallbacks](#/kb/prod-fallbacks), [Health checks](#/kb/prod-health-checks).
- **Model code**: no leakage, same transformations at training and serving. [Train/serve skew](#/kb/prod-train-serve-skew), [Sklearn pipelines](#/kb/ml-sklearn-pipeline).

## Keeping control

- If the assistant adds a retry decorator, a class hierarchy or a config file nobody asked for, remove it and ask again for the function.
- If you cannot say what happens at the boundary (the exact second of expiry, the n-th attempt), run it and look.
- If a test fails, read the failing line first and decide whether the code or the expectation is wrong.
- After the piece works, explain it aloud as you would to an interviewer: what it does, which rule each line enforces, and what you would improve.

## Common mistakes

- Asking for the whole component in one prompt and accepting a design you did not choose.
- Testing only the success path.
- Using the real clock or real randomness, which makes tests flaky.
- Letting the assistant catch `Exception` "for robustness".

## Related

- [Determinism](#/kb/prod-determinism)
- [Structured logging](#/kb/prod-structured-logging)
- [Circuit breaker](#/kb/prod-circuit-breaker)
- [Verifying AI-written code](#/kb/ai-verifying-ai-code)
