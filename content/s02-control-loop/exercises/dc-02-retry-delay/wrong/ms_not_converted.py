def retry(fn, *, attempts, base_ms, cap_ms, sleep):
    # computes the delay itself and forgets that sleep wants seconds
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception:
            if attempt == attempts:
                raise
            sleep(min(base_ms * 2 ** (attempt - 1), cap_ms))
