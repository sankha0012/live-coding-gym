from backoff import backoff_delay


def retry(fn, *, attempts, base_ms, cap_ms, sleep):
    for attempt in range(attempts):
        try:
            return fn()
        except Exception:
            if attempt == attempts - 1:
                raise
            sleep(backoff_delay(attempt, base_ms, cap_ms))
