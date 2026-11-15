class TransientError(Exception):
    pass


def call_with_retry(fn, retries, sleep, base_delay=1.0):
    attempt = 0
    while True:
        try:
            return fn()
        except (TimeoutError, ConnectionError, TransientError):
            if attempt >= retries:
                raise
            sleep(base_delay)
            attempt += 1
