def dedupe_events(events, key="id"):
    seen = set()
    unique = []
    for event in events:
        if event[key] in seen:
            continue
        seen.add(event[key])
        unique.append(event)
    return unique, len(events) - len(unique)
