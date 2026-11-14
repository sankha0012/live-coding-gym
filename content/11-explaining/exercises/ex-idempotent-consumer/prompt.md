```python
class Consumer:
    """Apply each event once, even if the broker delivers it twice."""

    def __init__(self, handler):
        self.handler = handler
        self.seen = set()

    def process(self, event):
        key = event["id"]
        if key in self.seen:
            return False
        self.handler(event)
        self.seen.add(key)
        return True


def run(consumer, events):
    applied = 0
    for event in events:
        if consumer.process(event):
            applied += 1
    return applied


if __name__ == "__main__":
    balance = {"total": 0}

    def add(event):
        balance["total"] += event["amount"]

    consumer = Consumer(add)
    events = [
        {"id": "e1", "amount": 10},
        {"id": "e2", "amount": 5},
        {"id": "e1", "amount": 10},
    ]
    print(run(consumer, events), balance)
    print(run(consumer, events), balance)

    def flaky(event):
        balance["total"] += event["amount"]
        raise RuntimeError("crash after applying")

    c2 = Consumer(flaky)
    for _ in range(2):
        try:
            c2.process({"id": "x", "amount": 1})
        except RuntimeError:
            pass
    print(balance)
```

Explain this code as you would to the interviewer after finishing it: what it does, how, complexity, one risk.
