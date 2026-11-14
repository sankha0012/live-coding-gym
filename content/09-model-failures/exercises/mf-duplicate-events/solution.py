def dedupe_events(events):
    seen = set()
    unique = []
    for event in events:
        if event["id"] in seen:
            continue
        seen.add(event["id"])
        unique.append(event)
    return unique, len(events) - len(unique)
