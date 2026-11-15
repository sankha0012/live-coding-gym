LEVELS = {"debug", "info", "warning", "error"}
RESERVED = ("level", "event", "ts")


def make_record(level, event, fields, clock):
    if level not in LEVELS:
        raise ValueError(f"bad level: {level!r}")
    if not isinstance(event, str) or not event:
        raise ValueError("event must be a non-empty string")
    fields = fields or {}
    for key in RESERVED:
        if key in fields:
            raise ValueError(f"reserved key: {key}")
    return {"level": level, "event": event, "ts": clock(), **{k: v for k, v in fields.items() if v}}
