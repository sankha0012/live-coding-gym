# Idempotency and retries

## The problem it solves

Networks fail, jobs restart and queues deliver a message twice. The usual answer to a failure is to try again. But trying again is only safe if running the same work twice has the same effect as running it once. That property is called idempotency. Without it, a retry charges a customer twice, adds a row twice or counts an event twice.

So the two ideas go together: retry the work that is safe to repeat, and make the work safe to repeat.

## The smallest runnable example

```python
class Processor:
    def __init__(self):
        self._done = {}          # key -> stored result
        self.runs = 0

    def process(self, key, payload):
        if key in self._done:
            return self._done[key]       # repeat: return the stored result
        self.runs += 1
        result = payload * 2             # the real work
        self._done[key] = result         # store after the work succeeds
        return result


p = Processor()
assert p.process("order-1", 21) == 42
assert p.process("order-1", 21) == 42    # same key, no second run
assert p.runs == 1
print(p.runs)
```

The key identifies the request, not the payload. The client or the producer creates it once (an order id, a UUID) and sends the same key on every retry. The server checks the key before doing the work.

In real systems the dictionary is a database table with a unique constraint on the key, so two workers cannot both win.

## Retrying safely

```python
def call_with_retry(fn, attempts=3, transient=(TimeoutError, ConnectionError), sleep=lambda s: None):
    for i in range(attempts):
        try:
            return fn()
        except transient:
            if i == attempts - 1:
                raise                    # out of attempts: let the caller see it
            sleep(0.1 * 2 ** i)          # exponential backoff


state = {"n": 0}


def flaky():
    state["n"] += 1
    if state["n"] < 3:
        raise TimeoutError
    return "ok"


assert call_with_retry(flaky) == "ok"
try:
    call_with_retry(lambda: 1 / 0)
except ZeroDivisionError:
    print("not retried")
```

The rules of a good retry are short.

- Retry only transient errors: timeouts, connection resets, HTTP 429 and 503. A bad request (400) or a bug (`ZeroDivisionError`) will fail again, so retrying only wastes time.
- Wait longer each time (exponential backoff). Add random jitter in production so many clients do not retry at the same moment. Take the random generator as a parameter so tests stay deterministic.
- Set a limit on attempts or total time. An infinite retry loop is an outage you wrote yourself.
- Re-raise the last error when you give up. Do not return a fake success.

## Three traps people hit

1. **Retrying a non-idempotent call.** If a payment call times out, you do not know whether it went through. Retrying without an idempotency key can charge twice. Send the key, or do not retry.
2. **Storing the key before the work finishes.** If you record "done" and then crash, the retry sees the key and skips work that never happened. Store the result after success, or use a state such as "in progress" with a timeout.
3. **Retrying everything.** A catch-all `except Exception` in the retry loop also retries bugs and validation errors. Name the transient errors.

Another detail: the same key with a different payload is a client bug. Decide how to handle it. Raising an error is the safest answer.

## Duplicates and order in event streams

Message queues usually promise at-least-once delivery, so duplicates are normal. Idempotent handlers fix that. Events can also arrive out of order, so "last write wins" must use the event time (and an id as a tie-break), not the arrival order.

## Say it like this

"A retry is only safe if the operation is idempotent. So I give each request a key, and before doing the work I check whether that key was already processed. If it was, I return the stored result. I store the result only after the work succeeds. For retries, I catch only transient errors such as timeouts, use exponential backoff with a cap on attempts, inject the sleep so tests are fast, and re-raise the last error when I give up. Permanent errors fail immediately."
