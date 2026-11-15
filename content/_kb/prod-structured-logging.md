---
title: Structured logging
summary: Log one JSON object per event with fixed keys, so machines can filter and count without parsing prose.
tags: [production, logging]
---
```python
import json

def log_event(write, now, level, event, **fields):
    record = {"ts": now, "level": level, "event": event, **fields}
    write(json.dumps(record, sort_keys=True, default=str))   # one JSON object per line

lines = []
log_event(lines.append, 1700000000.0, "info", "batch_done", batch_id=7, rows=120, failed=2)
lines[0]
# '{"batch_id": 7, "event": "batch_done", "failed": 2, "level": "info", "rows": 120, "ts": 1700000000.0}'
```

- Use it for anything you will later search, count or alert on.
- Key rule: a constant event name plus key-value fields. Never glue values into the message text.
- Say: "I inject the writer and the timestamp, so the test asserts the exact line."

<!-- more -->

## Details

A text log like `"batch 7 done, 120 rows, 2 failed"` needs a regular expression to read. A structured record can be filtered with `event == "batch_done" and failed > 0`.

Good habits:

- **Stable event names.** `"batch_done"`, not `"Batch 7 finished"`. The variable parts go in fields.
- **Context ids.** Put `request_id`, `model_version` and `batch_id` on every line, so lines of one request can be joined.
- **`sort_keys=True`.** The output is deterministic and easy to compare in a test.
- **`default=str`.** A `datetime` or `Path` in a field becomes a string instead of raising `TypeError` in the logging path.
- **Levels.** `info` for normal events, `warning` for handled problems (a fallback was used), `error` for failures.

With the standard `logging` module, the same idea is a formatter:

```python
import io, logging

class JsonFormatter(logging.Formatter):
    def format(self, record):
        data = {"level": record.levelname, "event": record.getMessage()}
        data.update(getattr(record, "fields", {}))
        return json.dumps(data, sort_keys=True, default=str)

out = io.StringIO()
handler = logging.StreamHandler(out)
handler.setFormatter(JsonFormatter())
log = logging.getLogger("kb-demo")
log.addHandler(handler)
log.warning("fallback_used", extra={"fields": {"reason": "timeout"}})
out.getvalue()   # '{"event": "fallback_used", "level": "WARNING", "reason": "timeout"}\n'
```

Logs are for single events. For rates and latencies, also count them as metrics.

## Common mistakes

- Logging secrets, tokens or personal data. Log an id or a hash.
- Putting a NaN in a field: `json.dumps` writes `NaN`, which is not valid JSON for most readers.
- Using `print`, which has no level and cannot be redirected per module.
- Letting a logging error break the request. A log call must never raise to the caller.
- Logging a whole batch or payload on every line, which is costly and hard to read.

## See also

- [JSON: dumps, loads, sort_keys](#/kb/py-json)
- [Monitoring and latency percentiles](#/kb/prod-monitoring-percentiles)
- [Clocks: time.monotonic and injecting a clock or sleep](#/kb/py-time-clock-injection)
