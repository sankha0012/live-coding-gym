import functools


def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as err:
                    print(f"attempt {attempt} failed: {err}")
            raise RuntimeError(f"{func.__name__} gave up after {times} tries")
        return wrapper
    return decorator


calls = {"n": 0}


@retry(3)
def fetch():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("timeout")
    return "ok"


print(fetch())
print(fetch.__name__, calls["n"])
