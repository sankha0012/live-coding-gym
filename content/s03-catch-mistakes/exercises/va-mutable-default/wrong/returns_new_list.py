def record_event(event, log=None):
    if log is None:
        log = []
    return log + [event]
