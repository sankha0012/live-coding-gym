import time

def call_with_retry(fn, max_tries=3, base=1.0, sleep=None):
    if sleep is None:
        sleep = time.sleep
    for attempt in range(max_tries):
        try:
            return fn()
        except Exception:
            if attempt == max_tries - 1:
                raise
            sleep(2 ** attempt)
