LEVELS = {"debug", "info", "warning", "error"}


def make_record(level, event, fields, clock):
    if level not in LEVELS:
        raise ValueError(level)
    if not isinstance(event, str) or not event:
        raise ValueError("event")
    return {"level": level, "event": event, "ts": clock(), **(fields or {})}
