import time

def call_with_retry(fn, max_tries=3, base=1.0, sleep=None):
    if sleep is None:
        sleep = time.sleep
    first = None
    for attempt in range(max_tries):
        try:
            return fn()
        except Exception as e:
            first = first or e
            if attempt == max_tries - 1:
                raise first
            sleep(base * 2 ** attempt)
