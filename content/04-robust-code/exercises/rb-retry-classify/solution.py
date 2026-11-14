class TransientError(Exception):
    pass


TRANSIENT = (TimeoutError, ConnectionError, TransientError)


def call_with_retry(fn, retries, sleep, base_delay=1.0):
    attempt = 0
    while True:
        try:
            return fn()
        except TRANSIENT:
            if attempt >= retries:
                raise
            sleep(base_delay * 2 ** attempt)
            attempt += 1
