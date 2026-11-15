import time

def call_with_retry(fn, max_tries=3, base=1.0, sleep=None):
    if sleep is None:
        sleep = time.sleep
    for attempt in range(1, max_tries + 1):
        try:
            return fn()
        except Exception:
            if attempt == max_tries:
                raise
            sleep(base * 2 ** attempt)
