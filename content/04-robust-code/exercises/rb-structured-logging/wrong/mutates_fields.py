LEVELS = {"debug", "info", "warning", "error"}


def make_record(level, event, fields, clock):
    if level not in LEVELS:
        raise ValueError(level)
    if not isinstance(event, str) or not event:
        raise ValueError("event")
    fields = fields if fields is not None else {}
    for key in ("level", "event", "ts"):
        if key in fields:
            raise ValueError(key)
    fields["level"] = level
    fields["event"] = event
    fields["ts"] = clock()
    return fields
