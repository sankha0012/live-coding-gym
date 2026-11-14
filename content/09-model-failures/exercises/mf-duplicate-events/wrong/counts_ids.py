def dedupe_events(events):
    seen = set()
    dup_ids = set()
    unique = []
    for event in events:
        if event["id"] in seen:
            dup_ids.add(event["id"])
            continue
        seen.add(event["id"])
        unique.append(event)
    return unique, len(dup_ids)
