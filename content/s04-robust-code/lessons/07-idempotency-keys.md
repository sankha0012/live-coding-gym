# Idempotency keys

## What it is

An operation is idempotent when running it twice has the same effect as running it once. An idempotency key is an identifier, created once by the caller and sent with every retry of the same request, that lets the receiver recognise a repeat and return the stored result instead of doing the work again. See [Idempotency](#/kb/prod-idempotency) and [Event deduplication and ordering](#/kb/prod-event-dedup-ordering).

## How it breaks in production

Queues deliver at least once, jobs restart, and clients retry after a timeout without knowing whether the first call worked. Without a key, a retried payment charges twice, a retried insert adds a duplicate row, and a replayed event is counted twice in a metric. Keys themselves go wrong in three ways. If you record the key as done before the work finishes and then crash, the retry skips work that never happened. If two workers check the key at the same moment, both see "not done" and both run, so the check needs a unique constraint or a lock in the real store. And a reused key with a different payload is a client bug that silently returning the old result would hide.

## The defence in code

```python
import hashlib
import json


class KeyConflict(Exception):
    pass


class Processor:
    def __init__(self):
        self.done = {}     # key -> (payload fingerprint, result); a table with a unique key in real life
        self.runs = 0

    def process(self, key, payload):
        fp = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
        if key in self.done:
            old_fp, result = self.done[key]
            if old_fp != fp:
                raise KeyConflict(key)          # same key, different request
            return result                       # repeat: stored result, no new work
        self.runs += 1
        result = payload["x"] * 2               # the real work
        self.done[key] = (fp, result)           # recorded only after it succeeded
        return result


p = Processor()
assert p.process("order-1", {"x": 21}) == 42
assert p.process("order-1", {"x": 21}) == 42
assert p.runs == 1
try:
    p.process("order-1", {"x": 5})
except KeyConflict:
    print("conflict detected")
```

The key identifies the request, not the payload, and the caller generates it once, for example an order id or a UUID. The fingerprint of the payload catches key reuse. The result is stored only after the work succeeds.

## What to say in the interview

"A retry is only safe if the operation is idempotent, so each request carries a key from the caller. Before doing the work I look the key up and, if it exists, return the stored result. I store it after success, never before, and I compare a payload fingerprint so a reused key with different data raises an error. In a real system the lookup is a unique constraint in the database, so two workers cannot both win."
