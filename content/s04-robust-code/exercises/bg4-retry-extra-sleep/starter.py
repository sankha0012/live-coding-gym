class TransientError(Exception):
    pass


def call_with_retry(fn, retries, sleep, base_delay=1.0):
    last = None
    for attempt in range(retries + 1):
        try:
            return fn()
        except (TimeoutError, ConnectionError, TransientError) as exc:
            last = exc
            sleep(base_delay * 2 ** attempt)
    raise last
