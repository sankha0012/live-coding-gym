class TransientError(Exception):
    pass


TRANSIENT = (TimeoutError, ConnectionError, TransientError)


def call_with_retry(fn, retries, sleep, base_delay=1.0, max_delay=None):
    attempt = 0
    while True:
        try:
            return fn()
        except TRANSIENT:
            if attempt >= retries:
                raise
            delay = base_delay * 2 ** attempt
            if max_delay is not None:
                delay = min(delay, max_delay)
            sleep(delay)
            attempt += 1
