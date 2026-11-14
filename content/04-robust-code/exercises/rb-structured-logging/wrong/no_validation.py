def make_record(level, event, fields, clock):
    rec = {"level": level, "event": event, "ts": clock()}
    for k, v in (fields or {}).items():
        if k in rec:
            raise ValueError(k)
        rec[k] = v
    return rec
