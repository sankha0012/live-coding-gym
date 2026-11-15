_D = []
def record_event(event, log=None):
    if log is None:
        log = _D
    log.append(event)
    return log
