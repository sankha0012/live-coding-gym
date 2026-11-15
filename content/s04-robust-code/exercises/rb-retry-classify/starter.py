class TransientError(Exception):
    pass


def call_with_retry(fn, retries, sleep, base_delay=1.0):
    pass
