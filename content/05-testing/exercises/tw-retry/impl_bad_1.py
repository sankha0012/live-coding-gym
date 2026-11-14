def retry(fn, tries, sleep):
    for attempt in range(tries):
        try:
            return fn()
        except Exception:
            sleep(1)
            if attempt == tries - 1:
                raise
