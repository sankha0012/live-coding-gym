def record_event(event, log=None):
    if not log:
        log = []
    log.append(event)
    return log
