def record_event(event, log=None):
    """Append event to log and return log.

    If log is passed, append in place and return that same list.
    If log is not passed, start a fresh empty list on every call.
    """
    if log is None:
        log = []
    log.append(event)
    return log
