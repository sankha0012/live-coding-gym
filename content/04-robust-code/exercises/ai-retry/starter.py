import time

def call_with_retry(fn, max_tries=3, base=1.0, sleep=None):
    if sleep is None:
        sleep = time.sleep
    pass
