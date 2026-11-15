import time

def call_with_retry(fn, max_tries=3, base=1.0, sleep=None):
    if sleep is None:
        sleep = time.sleep
    for attempt in range(3):
        try:
            return fn()
        except Exception:
            if attempt == 2:
                raise
            sleep(base * 2 ** attempt)
