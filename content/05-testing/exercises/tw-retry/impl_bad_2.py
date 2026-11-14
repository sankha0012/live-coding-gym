def retry(fn, tries, sleep):
    for attempt in range(tries - 1):
        try:
            return fn()
        except Exception:
            if attempt == tries - 2:
                raise
            sleep(1)
