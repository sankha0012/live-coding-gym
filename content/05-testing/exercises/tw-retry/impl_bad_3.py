def retry(fn, tries, sleep):
    for attempt in range(tries):
        try:
            return fn()
        except Exception:
            if attempt < tries - 1:
                sleep(1)
