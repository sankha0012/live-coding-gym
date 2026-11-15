# Structured logging

## What it is

A structured log record is a set of named fields, usually one JSON object per line, instead of a free-text sentence. Every record carries the same fields, such as time, level, event name, and the ids that identify the request or batch. Tools can then filter, count and alert on fields without parsing English. See [Structured logging](#/kb/prod-structured-logging) and [Monitoring](#/kb/tool-monitoring).

## How it breaks in production

Free-text logs such as "failed to score user 123, using fallback" cannot be counted reliably: the wording changes, the number is buried in the sentence, and a grep misses variations. Without ids you cannot connect the log lines of one request. Logging only the exception and not the context ("KeyError: 'age'") tells you nothing about which record caused it. The opposite error is logging everything per row, which floods storage and hides the signal, or logging personal data and secrets such as tokens and emails. The worst case is a silent fallback: the code recovers and says nothing, so a model that quietly falls back on 40 percent of requests looks healthy.

## The defence in code

```python
import json
import logging


class JsonFormatter(logging.Formatter):
    def format(self, record):
        entry = {"level": record.levelname, "event": record.getMessage()}
        entry.update(getattr(record, "fields", {}))
        return json.dumps(entry, sort_keys=True)


class ListHandler(logging.Handler):         # collects lines so a test can read them
    def __init__(self):
        super().__init__()
        self.lines = []

    def emit(self, record):
        self.lines.append(self.format(record))


handler = ListHandler()
handler.setFormatter(JsonFormatter())
log = logging.getLogger("scoring")
log.addHandler(handler)
log.setLevel(logging.INFO)
log.propagate = False

fallbacks = 0
for user_id in ["u1", "u2"]:
    try:
        raise TimeoutError("model slow")
    except TimeoutError as e:
        fallbacks += 1
        log.warning("fallback_used", extra={"fields": {"user_id": user_id, "reason": str(e)}})
log.info("batch_done", extra={"fields": {"rows": 2, "fallbacks": fallbacks}})

assert json.loads(handler.lines[-1]) == {
    "level": "INFO", "event": "batch_done", "rows": 2, "fallbacks": 2}
print(handler.lines[0])
```

Each line parses as JSON, the event name is stable, and the batch summary carries the counts, so an alert can fire when `fallbacks / rows` rises. The test reads the lines back instead of eyeballing output. Log one summary per batch and individual records only for errors, and never log secrets.

## What to say in the interview

"I log events as JSON with a stable event name and the ids needed to trace a request, not as free-text sentences. Every fallback, retry or skipped row is counted and logged, with a summary per batch so I can alert on the rate. I avoid logging per row at scale and I never log secrets or personal data. In tests I capture the log lines and assert on the fields."
