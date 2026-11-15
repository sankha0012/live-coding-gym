---
title: Idempotency and idempotency keys
summary: Make a repeated request safe by remembering the result under a key, so the side effect happens once.
tags: [production, reliability]
---
```python
class IdempotentStore:
    def __init__(self):
        self.done = {}                   # key -> saved result

    def apply(self, key, action):
        if key in self.done:
            return self.done[key]        # repeat: no second side effect
        result = action()
        self.done[key] = result          # record only after success
        return result
```

- Use it whenever a caller may retry: payments, emails, writes, queue consumers.
- Key rule: the same key returns the first result and never runs the action again.
- Say: "Retries and at-least-once delivery mean duplicates, so I make the operation idempotent with a key."

<!-- more -->

## Details

An operation is idempotent when doing it twice has the same effect as doing it once. `x = 5` is idempotent. `x += 1` is not. When the operation is not naturally idempotent, an idempotency key makes it so.

```python
store, sent = IdempotentStore(), []

def send():
    sent.append("email")
    return "sent"

store.apply("order-42:confirm", send)   # 'sent'
store.apply("order-42:confirm", send)   # 'sent'   answered from the store
sent                                    # ['email']  one side effect
```

Where the key comes from:

- The caller sends it (a request id), and reuses it on every retry.
- You derive it from the content, for example a `hashlib` digest of the canonical JSON. Then two identical requests count as one, which must be what you want.

If the action raises, nothing is stored, so a retry runs it again. That is usually right for transient errors.

In a real system the store is a database table with a unique constraint on the key, and "check then write" must be one atomic step. Otherwise two workers can both pass the check. Keys also need an expiry, or the store grows without limit.

## Common mistakes

- Testing `if self.done.get(key)`: a stored result of `None`, `0` or `""` looks like "not done". Use `key in`.
- Storing the key before the action succeeds, so a failed action can never be retried.
- Building the key from a timestamp or a random value, so each retry gets a new key.
- Running the action again for a repeat and only skipping the save.

## See also

- [Retries with backoff](#/kb/prod-retry-backoff)
- [Duplicate and out-of-order events](#/kb/prod-event-dedup-ordering)
- [Stable hashing with hashlib (and why not hash())](#/kb/py-hashlib)
