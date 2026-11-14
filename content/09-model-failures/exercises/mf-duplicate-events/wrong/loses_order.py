def dedupe_events(events):
    first = {}
    for event in events:
        first.setdefault(event["id"], event)
    unique = sorted(first.values(), key=lambda e: str(e["id"]))
    return unique, len(events) - len(unique)
