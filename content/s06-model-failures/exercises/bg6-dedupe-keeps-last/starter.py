def dedupe_events(events):
    by_id = {}
    for event in events:
        by_id[event["id"]] = event
    return list(by_id.values()), len(events) - len(by_id)
