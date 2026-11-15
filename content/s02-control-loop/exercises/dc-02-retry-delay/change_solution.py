from backoff import backoff_delay


def retry(fn, *, attempts, base_ms, cap_ms, sleep, factor=2):
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception:
            if attempt == attempts:
                raise
            sleep(backoff_delay(attempt, base_ms, cap_ms, factor))
